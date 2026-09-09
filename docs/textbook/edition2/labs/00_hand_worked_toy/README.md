# Lab 0 — Hand-calculable toy analysis

Status: **executed successfully**. Runtime category: seconds.

This redistributable six-variant, four-vector example demonstrates metadata removal, variants-by-vectors to vectors-by-variants orientation, implemented average-rank RINT, Euclidean distance, two-cluster silhouette, the exact `legacy_dimple` scoring implementation with and without a noise term, and exact versus permutation-invariant labels. It deliberately does not claim to reproduce UMAP by hand.

Run `docs/textbook/edition2/build/runtime_env/bin/python docs/textbook/edition2/labs/00_hand_worked_toy/run_hand_worked.py` from the Freeze 3 root into a fresh `executed_output` directory. The retained record reports a 4×6 analysis matrix, silhouette 0.924591, numeric inequality for relabeled partitions, and ARI/NMI 1.0. Inspect the RINT table and both candidate tables before the JSON summary.
