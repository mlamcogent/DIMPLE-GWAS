#!/usr/bin/env python3
"""
generate_idp_key.py

Utility to generate a standardized IDP_KEY.csv (or generic feature key) used by DIMPLE-GWAS.

Input: a feature metadata table containing *at least* three columns:
  - index (feature index used in your embeddings/X matrix)
  - feature_name (human-readable feature label)
  - feature_category_name (group/category for reporting/plots)

Output: CSV with columns exactly:
  index,feature_name,feature_category_name

Examples:
  # Excel input
  python generate_idp_key.py \
    --input Hapmap_SNPs_original_ldsc_IDP_UMAP_DBSCAN_Cluster_details.xlsx \
    --sheet 0 \
    --index-col index \
    --name-col "original_IDP" \
    --category-col "original_Category name" \
    --output IDP_KEY.csv

  # CSV input
  python generate_idp_key.py \
    --input feature_metadata.csv \
    --index-col feature_index \
    --name-col feature_name \
    --category-col category \
    --output IDP_KEY.csv
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

import pandas as pd


def _read_table(path: str, sheet: Optional[str], delimiter: Optional[str]) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()

    if ext in [".xlsx", ".xls"]:
        return pd.read_excel(path, sheet_name=sheet if sheet is not None else 0)

    if ext in [".csv", ".tsv", ".txt"]:
        # delimiter: if explicitly provided, use it; else infer based on extension
        sep = delimiter if delimiter is not None else ("\t" if ext in [".tsv"] else ",")
        return pd.read_csv(path, sep=sep)

    if ext in [".parquet"]:
        return pd.read_parquet(path)

    raise ValueError(
        f"Unsupported input type '{ext}'. Supported: .xlsx/.xls, .csv, .tsv/.txt, .parquet"
    )


def _fail(msg: str, exit_code: int = 2) -> None:
    print(f"[generate_idp_key] ERROR: {msg}", file=sys.stderr)
    sys.exit(exit_code)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate standardized IDP_KEY.csv from a feature metadata table."
    )
    ap.add_argument("--input", required=True, help="Path to metadata table (xlsx/csv/tsv/parquet).")
    ap.add_argument("--output", default="IDP_KEY.csv", help="Output CSV path. Default: IDP_KEY.csv")

    ap.add_argument("--sheet", default=None,
                    help="Excel sheet name or index (e.g. 'Sheet1' or '0'). Only for .xlsx/.xls.")

    ap.add_argument("--delimiter", default=None,
                    help="Delimiter for CSV/TSV if not standard. Example: ',' or '\\t'.")

    ap.add_argument("--index-col", required=True, help="Column name containing the feature index.")
    ap.add_argument("--name-col", required=True, help="Column name containing the feature name.")
    ap.add_argument("--category-col", required=True, help="Column name containing the category name.")

    ap.add_argument("--drop-missing", action="store_true",
                    help="Drop rows with missing index/name/category instead of failing.")
    ap.add_argument("--allow-duplicate-index", action="store_true",
                    help="Allow duplicate indices (not recommended). Default is to fail.")
    ap.add_argument("--coerce-index-int", action="store_true",
                    help="Attempt to coerce index column to integer (useful if read as float).")

    ap.add_argument("--strip", action="store_true",
                    help="Strip leading/trailing whitespace from name/category fields.")
    ap.add_argument("--sort-by-index", action="store_true",
                    help="Sort output by index ascending.")

    args = ap.parse_args()

    # Read input
    sheet = args.sheet
    if sheet is not None:
        # allow numeric string sheet indices, e.g. "0"
        if isinstance(sheet, str) and sheet.isdigit():
            sheet = int(sheet)

    try:
        df = _read_table(args.input, sheet=sheet, delimiter=args.delimiter)
    except Exception as e:
        _fail(f"Failed to read input '{args.input}': {e}")

    # Validate presence of required columns
    missing = [c for c in [args.index_col, args.name_col, args.category_col] if c not in df.columns]
    if missing:
        _fail(
            "Missing required column(s): "
            + ", ".join(missing)
            + f"\nAvailable columns: {list(df.columns)}"
        )

    out = df[[args.index_col, args.name_col, args.category_col]].copy()
    out.columns = ["index", "feature_name", "feature_category_name"]

    if args.strip:
        out["feature_name"] = out["feature_name"].astype(str).str.strip()
        out["feature_category_name"] = out["feature_category_name"].astype(str).str.strip()

    if args.coerce_index_int:
        # common case: Excel reads integers as floats if there are NaNs
        try:
            out["index"] = pd.to_numeric(out["index"], errors="raise").astype("Int64")
        except Exception as e:
            _fail(f"Failed to coerce index to integer. Use without --coerce-index-int. Details: {e}")

    # Missingness checks
    if not args.drop_missing:
        if out["index"].isna().any():
            _fail("Found missing values in 'index'. Use --drop-missing to drop them.")
        if out["feature_name"].isna().any():
            _fail("Found missing values in 'feature_name'. Use --drop-missing to drop them.")
        if out["feature_category_name"].isna().any():
            _fail("Found missing values in 'feature_category_name'. Use --drop-missing to drop them.")
    else:
        before = len(out)
        out = out.dropna(subset=["index", "feature_name", "feature_category_name"])
        after = len(out)
        if after < before:
            print(f"[generate_idp_key] Dropped {before - after} rows with missing values.", file=sys.stderr)

    # Duplicates
    if not args.allow_duplicate_index:
        dup = out["index"].duplicated(keep=False)
        if dup.any():
            examples = out.loc[dup, "index"].astype(str).unique()[:10]
            _fail(
                "Duplicate feature indices found in 'index'. "
                "This typically breaks feature re-identification.\n"
                f"Example duplicate indices: {', '.join(examples)}\n"
                "Use --allow-duplicate-index if you are certain duplicates are acceptable."
            )

    if args.sort_by_index:
        # Works for numeric or string indices
        out = out.sort_values(by="index", kind="mergesort")

    # Write output
    try:
        out.to_csv(args.output, index=False)
    except Exception as e:
        _fail(f"Failed to write output '{args.output}': {e}")

    print(f"[generate_idp_key] Wrote {len(out)} rows to {args.output}")


if __name__ == "__main__":
    main()