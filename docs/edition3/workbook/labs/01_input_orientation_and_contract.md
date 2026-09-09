# Lab 1 - Input orientation, identifiers, and the data contract

**Evidence status:** input contract verified by source/tests; the small table below is illustrative.

Create a paper table with two metadata columns, three variant rows, and two numeric phenotype columns. Draw the table after metadata removal and transposition. Confirm that the two phenotype identifiers become the two rows being clustered.

Then inspect the retained synthetic input:

```text
benchmarks/synthetic/synthetic_matrix.tsv
benchmarks/synthetic/synthetic_annotations.csv
```

Check the header, delimiter, row count, metadata prefix, number of analysis columns, identifier source, non-numeric values, missingness, and annotation join key. The fixed contract produces 24 vectors by 80 numeric variables after four metadata columns are removed.

Resolve the tutorial configuration without fitting:

```bash
python -m dimple_gwas inspect-config \
  --search-mode fixed \
  --config docs/textbook/edition2/labs/01_fixed_synthetic/tutorial_config.yaml
```

**Decision checkpoint:** explain why a numeric, correctly oriented matrix can still fail scientific harmonization. Name the external provenance record that would establish allele, scale, overlap, ancestry, and QC choices.

**Failure exercise:** imagine one phenotype column contains a string value. Predict whether coercion should fail, silently drop the row, or impute. Verify the contract in the preprocessing reference; do not modify the authoritative fixture.

\newpage
