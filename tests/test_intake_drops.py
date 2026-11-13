"""Explicit metadata removal without orientation or preprocessing inference."""
import copy
import csv
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'bin'))
import matrix_intake as intake


class IntakeDrops(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.ids = ['001', 'NA', '東京'] + [f'object_{i}' for i in range(48)]

    def matrix(self, transposed=False, compressed=False):
        path = self.root / ('transpose.csv' if transposed else 'matrix.csv')
        with path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.writer(handle)
            if transposed:
                writer.writerow(['SNP ID', *self.ids])
                writer.writerow(['rs001', *range(51)])
                writer.writerow(['rs002', *[2 * i for i in range(51)]])
            else:
                writer.writerow(['label', 'f1', 'object_id', 'f2', 'notes'])
                writer.writerows([['case', i, oid, 2 * i, ''] for i, oid in enumerate(self.ids)])
        if compressed:
            path.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
        return path

    def test_objects_preserve_ids_values_and_raw_hash(self):
        for compressed in (False, True):
            with self.subTest(compressed=compressed):
                path = self.matrix(compressed=compressed)
                grid = intake.create_grid(path, 'objects_by_features', 'object_id', 'none', None,
                                          drop_columns=['label', 'notes'])
                contract = grid['input_contract']
                self.assertEqual(contract['drop_columns'], ['label', 'notes'])
                self.assertEqual(contract['expected_shape'], [51, 2])
                self.assertEqual(contract['sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
                ids, values = intake.verify_input(path, contract)
                self.assertEqual(ids, self.ids)
                self.assertEqual(values, [[float(i), float(2*i)] for i in range(51)])
                self.assertEqual(contract['scaling'], 'none')
                self.assertEqual(contract['missing_values'], 'reject')

    def test_transposed_snps_removed_before_numeric_validation(self):
        for compressed in (False, True):
            path = self.matrix(transposed=True, compressed=compressed)
            grid = intake.create_grid(path, 'features_by_objects', None, 'none', None,
                                      drop_columns=['SNP ID'])
            contract = grid['input_contract']
            ids, values = intake.verify_input(path, contract)
            self.assertEqual(ids, self.ids)
            self.assertEqual(contract['expected_shape'], [51, 2])
            self.assertEqual(values, [list(map(float, range(51))), [float(2*i) for i in range(51)]])
            with self.assertRaisesRegex(ValueError, 'object IDs already'):
                intake.inspect_matrix(path, 'features_by_objects', 'SNP ID', drop_columns=['SNP ID'])

    def test_no_automatic_drop_or_orientation_guess(self):
        for transposed, orientation, column in [(False, 'objects_by_features', 'object_id'),
                                                (True, 'features_by_objects', None)]:
            with self.assertRaisesRegex(ValueError, 'MANUAL.md'):
                intake.create_grid(self.matrix(transposed), orientation, column, 'none', None)
        with self.assertRaisesRegex(ValueError, 'orientation is never inferred'):
            intake.inspect_matrix(self.matrix(), None, 'object_id')

    def test_reject_unknown_duplicate_invalid_and_id_drops(self):
        path = self.matrix()
        for drops in (['unknown'], ['label', 'label'], ['object_id'], 'label', [1], [' label']):
            with self.subTest(drops=drops), self.assertRaises(ValueError):
                intake.inspect_matrix(path, 'objects_by_features', 'object_id', drop_columns=drops)
        with self.assertRaisesRegex(ValueError, 'one feature'):
            intake.inspect_matrix(path, 'objects_by_features', 'object_id',
                                  drop_columns=['label', 'notes', 'f1', 'f2'])

    def test_retained_missing_values_and_malformed_rows_rejected(self):
        path = self.matrix()
        original = path.read_text()
        path.write_text(original.replace('case,0,001,0,', 'case,,001,0,'))
        with self.assertRaisesRegex(ValueError, 'MANUAL.md'):
            intake.inspect_matrix(path, 'objects_by_features', 'object_id', drop_columns=['label', 'notes'])
        path.write_text(original.replace('case,0,001,0,', 'case,0,001,0'))
        with self.assertRaisesRegex(ValueError, 'wrong field count'):
            intake.inspect_matrix(path, 'objects_by_features', 'object_id', drop_columns=['label', 'notes'])

    def test_default_contract_unchanged_and_optional_field_validated(self):
        path = ROOT / 'examples/synthetic-matrix.csv'
        original = intake.create_grid(path, 'objects_by_features', 'object_id', 'none', None)
        self.assertNotIn('drop_columns', original['input_contract'])
        self.assertEqual(original, intake.create_grid(path, 'objects_by_features', 'object_id', 'none', None, []))
        contract = copy.deepcopy(original['input_contract'])
        contract['drop_columns'] = []
        self.assertEqual(intake.verify_input(path, contract), intake.verify_input(path, original['input_contract']))
        for invalid in (None, 'label', [False], ['x', 'x']):
            contract['drop_columns'] = invalid
            with self.assertRaises(ValueError):
                intake.validate_contract(contract)
        contract = copy.deepcopy(original['input_contract'])
        contract['unexpected'] = []
        with self.assertRaises(ValueError):
            intake.validate_contract(contract)

    def test_optional_science_config_preserves_original_mapping(self):
        from science_config import resolved_science
        config = self.root / 'science.json'
        science = {'backend': 'umap', 'execution': {'n_random_states': 5}}
        config.write_text(json.dumps(science))
        grid = intake.create_grid(self.matrix(), 'objects_by_features', 'object_id', 'none', None,
                                  drop_columns=['label', 'notes'], config=config)
        self.assertEqual(grid['science'], science)
        self.assertEqual(resolved_science(grid)['backend'], 'umap')
        config.write_text('{"unknown_setting": true}')
        with self.assertRaises(ValueError):
            intake.create_grid(self.matrix(), 'objects_by_features', 'object_id', 'none', None,
                               drop_columns=['label', 'notes'], config=config)

    def test_cli_records_exact_named_drops_and_supports_repetition(self):
        path = self.matrix()
        output = self.root / 'grid.json'
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'bin/matrix_intake.py'),
                                 '--matrix', str(path), '--orientation', 'objects_by_features',
                                 '--object-id-column', 'object_id', '--preprocessing', 'none',
                                 '--drop-columns', 'label', '--drop-columns', 'notes', '--output', str(output)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(output.read_text())['input_contract']['drop_columns'], ['label', 'notes'])


if __name__ == '__main__':
    unittest.main()
