#!/bin/bash

runcard_path="/app/runcards/monitor.yml"
report_path="/app/report"
exporter_script_path="/app/scripts/metrics_export.py"

if [[ $# == 0 ]];
then
    echo Running locally
    qq auto ${runcard_path} -o ${report_path} -f; python3 ${exporter_script_path}
    exit
elif [[ $# == 1 ]];
then
    echo preparing slurm script
    slurm_partition=$1
else
    echo too many arguments
    exit
fi

platform=$slurm_partition

echo "#!/bin/bash" > monitoring_slurm_script
echo "#SBATCH -J monitoring_${platform}" >> monitoring_slurm_script
echo "#SBATCH -p ${slurm_partition}" >> monitoring_slurm_script
echo "#SBATCH -o slurm.out" >> monitoring_slurm_script
echo "" >> monitoring_slurm_script
echo "qq auto ${runcard_path} -o ${report_path} -f" >> monitoring_slurm_script

# run the exporter locally
if [[ -z $(squeue -p ${slurm_partition} -u $USER -n monitoring_${platform} | sed '1d') ]];
then
    sbatch -W --parsable monitoring_slurm_script
    wait
    python3 ${exporter_script_path}
else
    echo "Another job is currently running for ${platform} on ${partition}"
fi
