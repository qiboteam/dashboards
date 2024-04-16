#!/bin/bash

# run the exporter locally
if [[ $(squeue -p {{ slurm_partition }} -u '$USER' -n monitoring_{{ platform }} | sed '1d') == "" ]];
then
    sbatch -W monitor.sh
    wait
else
    echo "Another job is currently running for {{ platform }} on {{ slurm_partition }}"
fi
