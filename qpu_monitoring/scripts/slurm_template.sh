#!/bin/bash
#SBATCH -J monitoring_{{ platform }}
#SBATCH -p {{ slurm_partition }}
#SBATCH -o slurm.out

qq auto {{ runcard_path }} -o {{ report_path }} -f
