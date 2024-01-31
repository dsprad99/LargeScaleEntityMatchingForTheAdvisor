#!/bin/bash
#SBATCH --partition=Orion
#SBATCH --job-name=theAdvisor
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --mem=100GB
#SBATCH --time=1:20:00


echo "======================================================"
echo "Start Time : $(date)"
echo "Submit Dir : $SLURM_SUBMIT_DIR"
echo "Job ID/Name : $SLURM_JOBID / $SLURM_JOB_NAME"
echo "Num Tasks : $SLURM_NTASKS total [$SLURM_NNODES nodes @ $SLURM_CPUS_ON_NODE CPUs/node]"
echo "======================================================"
echo ""

cd $SLURM_SUBMIT_DIR

parallel --link python matchingScript.py --start {1} --end {2} --fileName testing_parallel_matching_script ::: 0 101 151 ::: 1$echo ""
echo "======================================================"
echo "End Time : $(date)"
echo "======================================================"
