#!/bin/bash

nextflow run $ORSON_PATH/main.nf \
  --fasta $1 \
  --query_type p \
  --downloadDB_enable false \
  --busco_enable true \
  --lineage eukaryota_odb10,auto-lineage \
  --busco_db $BUSCO_DB_PATH \
  --beedeem_annot_enable true \
  --hit_tool diamond \
  --blast_db $BLAST_DB_PATH \
  -profile custom,singularity \
  --chunk_size 200 \
  -c $CLUSTER_CONFIG_PATH \
  --outdir ./results \
  -w $SCRATCH_WORK_DIR \
  --projectName func_annot_orson \
  -ansi-log false \
  -resume \
  ${3- } ${4- } \
  ${5- } ${6- }

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";
python3 $SCRIPT_DIR/add_fa_description.py --infile $1 --outfile ./results/03_final_results/described_fasta.fa --annotfile ./results/03_final_results/result.emapper.annotations
python3 $SCRIPT_DIR/add_gff_description.py --gffFile $2 --outFile ./results/03_final_results/described_gff.gff --eggFile ./results/03_final_results/result.emapper.annotations

cd ./results/02_intermediate_data/00_busco/busco_results_auto
ln -sf short_summary.specific.*.busco_results_auto.json short_summary.specific.busco_results_auto.json
ln -sf short_summary.specific.*.busco_results_auto.txt short_summary.specific.busco_results_auto.txt
