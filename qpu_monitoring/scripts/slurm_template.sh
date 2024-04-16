#!/bin/bash
#SBATCH -J monitoring_{{ platform }}
#SBATCH -p {{ slurm_partition }}
#SBATCH -o slurm.out

export QIBOLAB_PLATFORMS=~/qibolab_platforms_qrc
qq auto {{ runcard_path }} --platform {{ platform }} -o {{ report_path }} -f
