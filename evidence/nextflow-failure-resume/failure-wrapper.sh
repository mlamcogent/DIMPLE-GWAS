#!/bin/bash
if [[ "$1" == research.py && "$2" == grid && ! -f 'WORKSPACE/validation/freeze5_2_paramfix_20261111/science_nextflow_reviewed/fail_once' ]]; then
 touch 'WORKSPACE/validation/freeze5_2_paramfix_20261111/science_nextflow_reviewed/fail_once'
 echo 'INTENTIONAL_ONCE_GRID_FAILURE' >&2
 exit 77
fi
exec 'WORKSPACE/validation/nextflow_dev1_20261026/local_env/bin/python' "$@"
