#!/bin/bash

# run the exporter locally
if [[ $(squeue -p {{ slurm_partition }} -u "$USER" -n monitoring_{{ platform }} | sed '1d') == "" ]];
then
    sbatch -W qpu_monitor_job.sh
    wait
    cat slurm.out
else
    echo "Another job is currently running for {{ platform }} on {{ slurm_partition }}"
    exit 1
fi
