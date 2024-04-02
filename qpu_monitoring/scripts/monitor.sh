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
else
    echo too many arguments
    exit
fi

echo "#!/bin/bash" > monitoring_slurm_script
echo "#SBATCH -p iqm5q" >> monitoring_slurm_script
echo "#SBATCH -o slurm.out" >> monitoring_slurm_script
echo "" >> monitoring_slurm_script
echo "qq auto ${runcard_path} -o ${report_path} -f" >> monitoring_slurm_script

echo "python3 ${exporter_script_path}" >> metrics_export_slurm_script

monitoring_job_id=$(sbatch --parsable monitoring_slurm_script)
sbatch --dependency=afterany:${monitoring_job_id} metrics_export_slurm_script
