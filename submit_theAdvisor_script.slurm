#!/bin/bash
#SBATCH --partition=Orion
#SBATCH --job-name=theAdvisor
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
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

#total amount of papers that our DBLP will build to to 6649168
total_paper_querying=6649168

#this is the paper that we will start running our program on
start_paper=200

#paper that we will end at
end_paper=300

#note the number of tasks per node is set as the partitions we have
partitions=$SLURM_CPUS_ON_NODE

#k-mer value were hashing
k_mer=7

#number of repeating mers want removed
repeating_kmer_remove=0

#number of top k-mers want removed
top_kmer_remove=1000

divided_work=$(((end_paper-start_paper) / partitions))

echo "DBLP Hashtable Size: $total_paper_querying"
echo "Partitions: $partitions"
echo "Divided Work/Partition: $divided_work"
echo "Start Paper: $start_paper"
echo "End Paper: $end_paper"
echo ""

start_values=()
end_values=()

for i in $(seq 0 $((partitions-1))); do
    start_values+=($((start_paper + $divided_work * $i)))
    end_values+=($((start_paper + $divided_work * ($i + 1))))
done

end_values[-1]=$end_paper

parallel --link python matchingScript.py --paperLimit {1} --start {2} --end {3} --kmer {4} --repeatingMersRemove {5} --topMersRemove {6} --fileName testing_parallel_matching_script ::: "$total_paper_querying" ::: "${start_values[@]}" ::: "${end_values[@]}" ::: "${k_mer}" ::: "${repeating_kmer_remove}" ::: "${top_kmer_remove}"
echo ""
echo "======================================================"
echo "End Time : $(date)"
echo "======================================================"
