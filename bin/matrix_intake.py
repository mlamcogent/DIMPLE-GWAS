"""The portable numeric CSV input contract, shared by preflight and PREPARE."""
import argparse
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import re

NUMBER = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?')
ORIENTATIONS = ('objects_by_features', 'features_by_objects')
MIN_OBJECTS = 51
GRID_FIELDS = ('baseline_config_id', 'configs')
ROOT = Path(__file__).resolve().parents[1]


def unique_pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique_pairs)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def save_new(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')


def checked_names(names, description):
    if not names or any(not name or name.strip() != name or not name.isprintable() for name in names):
        raise ValueError(f'{description} must be nonempty printable strings without edge whitespace')
    if len(set(names)) != len(names):
        raise ValueError(f'{description} must be unique')


def numbers(cells, row_number):
    for cell in cells:
        cell = cell.strip()
        if not NUMBER.fullmatch(cell):
            raise ValueError(f'non-numeric or missing feature in CSV row {row_number}; explicitly drop metadata columns or preprocess missing values yourself; see docs/MANUAL.md')
        number = float(cell)
        if not math.isfinite(number):
            raise ValueError(f'non-finite feature in CSV row {row_number}; preprocess missing/non-finite values yourself; see docs/MANUAL.md')
        yield number


def checked_drop_columns(drop_columns):
    if drop_columns is None:
        return []
    if not isinstance(drop_columns, list) or any(not isinstance(name, str) for name in drop_columns):
        raise ValueError('drop_columns must be a list of column names; see docs/MANUAL.md')
    if drop_columns:
        checked_names(drop_columns, 'drop_columns')
    return list(drop_columns)


def inspect_matrix(path, orientation, id_column, retain_values=False, drop_columns=None):
    if orientation not in ORIENTATIONS:
        raise ValueError('declare a supported matrix orientation; orientation is never inferred; see docs/MANUAL.md')
    raw = Path(path).read_bytes()
    payload = io.BytesIO(raw)
    if raw.startswith(b'\x1f\x8b'):
        payload = gzip.GzipFile(fileobj=payload)
    stream = io.TextIOWrapper(payload, encoding='utf-8', newline='')
    reader = csv.reader(stream, strict=True)
    header = next(reader, [])
    if header and header[0].startswith('\ufeff'):
        raise ValueError('save the CSV as UTF-8 without a byte order mark')
    checked_names(header, 'CSV headers')
    drops = checked_drop_columns(drop_columns)
    absent = [name for name in drops if name not in header]
    if absent:
        raise ValueError(f'declared drop columns are absent: {absent}; see docs/MANUAL.md')
    by_object = orientation == 'objects_by_features'
    if by_object and id_column in drops:
        raise ValueError('cannot drop the declared object ID column; see docs/MANUAL.md')
    keep_indices = [index for index, name in enumerate(header) if name not in drops]
    retained_header = [header[index] for index in keep_indices]
    if by_object:
        if id_column not in header:
            raise ValueError('declared object ID column is absent')
        id_index = header.index(id_column)
        ids = []
    else:
        if id_column is not None:
            raise ValueError('object IDs already come from headers in features_by_objects')
        ids = retained_header
    numeric_indices = [index for index in keep_indices if not by_object or index != id_index]
    values = []
    row_count = 0
    for row_number, row in enumerate(reader, 2):
        if len(row) != len(header):
            raise ValueError(f'CSV row {row_number} has the wrong field count')
        if by_object:
            ids.append(row[id_index])
        row_count += 1
        numeric = list(numbers((row[index] for index in numeric_indices), row_number))
        if retain_values:
            values.append(numeric)
    checked_names(ids, 'object IDs')
    features = len(retained_header) - 1 if by_object else row_count
    if len(ids) < MIN_OBJECTS or features < 1:
        raise ValueError(f'the fixed recipe requires at least {MIN_OBJECTS} objects and one feature')
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'expected_shape': [len(ids), features]}, ids, values


def validate_contract(contract):
    fields = {'profile', 'orientation', 'object_id_column', 'sha256', 'expected_shape',
              'preprocessing', 'missing_values', 'scaling'}
    if set(contract) not in (fields, fields | {'drop_columns'}) or contract['profile'] != 'numeric_matrix' or (
        contract['missing_values'] != 'reject' or contract['scaling'] != 'none'
    ):
        raise ValueError('invalid portable numeric matrix contract')
    if 'drop_columns' in contract and contract['drop_columns'] is None:
        raise ValueError('drop_columns must be a list of column names; see docs/MANUAL.md')
    checked_drop_columns(contract.get('drop_columns', []))
    if not re.fullmatch('[a-f0-9]{64}', contract['sha256']):
        raise ValueError('exact matrix SHA256 required')
    shape = contract['expected_shape']
    if not isinstance(shape, list) or len(shape) != 2 or any(type(value) is not int for value in shape):
        raise ValueError('expected shape must be an ordered pair of integer dimensions')
    prep = contract['preprocessing']
    if prep != {'kind': 'none'} and (
        set(prep) != {'kind', 'record_sha256'} or prep['kind'] != 'external'
        or not re.fullmatch('[a-f0-9]{64}', prep['record_sha256'])
    ):
        raise ValueError('declare no preprocessing or pin the external preprocessing record')


def verify_input(path, contract):
    validate_contract(contract)
    measured, ids, values = inspect_matrix(path, contract['orientation'], contract['object_id_column'], retain_values=True,
                                          drop_columns=contract.get('drop_columns', []))
    if any(measured[key] != contract[key] for key in measured):
        raise ValueError('matrix bytes or oriented shape differ from the intake contract')
    return ids, values


def create_grid(matrix, orientation, id_column, preprocessing, record, drop_columns=None, config=None):
    if (preprocessing == 'external') != bool(record):
        raise ValueError('supply a record file for external preprocessing only')
    prep = {'kind': preprocessing}
    if record:
        prep['record_sha256'] = hashlib.sha256(Path(record).read_bytes()).hexdigest()
    drops = checked_drop_columns(drop_columns)
    observed, _, _ = inspect_matrix(matrix, orientation, id_column, drop_columns=drops)
    contract = dict(observed, profile='numeric_matrix', orientation=orientation,
                    object_id_column=id_column, preprocessing=prep, missing_values='reject', scaling='none')
    if drops:
        contract['drop_columns'] = drops
    validate_contract(contract)
    recipe = load_json(ROOT / 'conf/recipe.json')
    grid = {**recipe, 'confirmed': True, 'input_contract': contract}
    if config is not None:
        from science_config import resolve_grid
        grid['science'] = load_json(config)
        return resolve_grid(grid, recipe)
    return grid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--matrix', type=Path, required=True)
    parser.add_argument('--orientation', choices=ORIENTATIONS, required=True)
    parser.add_argument('--object-id-column')
    parser.add_argument('--drop-columns', nargs='+', action='extend', default=[], metavar='NAME',
                        help='exact CSV header names to remove before numeric validation; never inferred')
    parser.add_argument('--preprocessing', choices=('none', 'external'), required=True)
    parser.add_argument('--preprocessing-record', type=Path)
    parser.add_argument('--config', type=Path, help='optional science-only JSON configuration; see docs/MANUAL.md')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        grid = create_grid(args.matrix, args.orientation, args.object_id_column,
                           args.preprocessing, args.preprocessing_record, drop_columns=args.drop_columns, config=args.config)
        save_new(args.output, grid)
    except (OSError, ValueError, csv.Error, EOFError) as error:
        parser.exit(2, f'Intake refused: {error}. See docs/MANUAL.md for the input contract and user-managed preprocessing.\n')
    print(json.dumps({'status': 'INPUT_CHECKED', 'shape': grid['input_contract']['expected_shape'],
                      'sha256': grid['input_contract']['sha256']}))


if __name__ == '__main__':
    main()
