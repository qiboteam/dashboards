#!/bin/bash
#SBATCH -J monitoring_{{ platform }}
#SBATCH -p {{ slurm_partition }}
#SBATCH -o slurm.out

export QIBOLAB_PLATFORMS={{ qibolab_platforms_path }}
python {{ monitoring_script_path }} --platform {{ platform }} --output {{ report_path }} --targets 0 1
