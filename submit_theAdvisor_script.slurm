#!/bin/bash
#SBATCH --partition=Orion
#SBATCH --job-name=theAdvisor
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=15
#SBATCH --mem=100GB
#SBATCH --time=1:20:00


echo "======================================================"
echo "Start Time : $(date)"
echo "Submit Dir : $SLURM_SUBMIT_DIR"
echo "Job ID/Name : $SLURM_JOBID / $SLURM_JOB_NAME"
echo "Num Tasks : $SLURM_NTASKS total [$SLURM_NNODES nodes @ $SLURM_CPUS_ON_NODE CPUs/node]"
echo "======================================================"
echo ""

#PYTHON=python
PYTHON=python3


#cd $SLURM_SUBMIT_DIR

#total amount of papers that our program will run on
total_paper_querying=1000
total_DBLP_papers=6649168

#this is the paper that we will start running our program on
start_paper=200

#note the number of tasks per node is set as the partitions we have
#partitions=$SLURM_CPUS_ON_NODE
partitions=4

divided_work=$((total_paper_querying / partitions))

echo "Total Paper Querying: $total_paper_querying"
echo "Partitions: $partitions"
echo "Divided Work: $divided_work"

start_values=()
end_values=()

for i in $(seq 0 $partitions); do
    start_values+=($((start_paper + $divided_work * $i)))
    end_values+=($((start_paper + $divided_work * ($i + 1))))
done

end_values[-1]=$((end_values[-1] + total_paper_querying - (divided_work * partitions)))

parallel --link ${PYTHON} matchingScript.py --paperLimit {1} --start {2} --end {3} --fileName testing_parallel_matching_script ::: "$total_DBLP_papers" ::: "${start_values[@]}" ::: "${end_values[@]}"
echo ""
echo "======================================================"
echo "End Time : $(date)"
echo "======================================================"
