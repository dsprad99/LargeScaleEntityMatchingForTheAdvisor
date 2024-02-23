#!/bin/bash
#SBATCH --partition=Orion
#SBATCH --job-name=theAdvisor
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=25GB
#SBATCH --time=1:40:00


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

#this is the paper that we will start querying our program 
#if querying DBLP recommended that you start from 0 due to parsing in XML format
start_paper=0

#paper that we will end at
end_paper=600000

#note the number of tasks per node is set as the partitions we have
partitions=$SLURM_CPUS_ON_NODE

#k-mer value were hashing
k_mer=7

#number of repeating mers want removed
repeating_kmer_remove=0

#number of top k-mers want removed
top_kmer_remove=1000

#pass in 0 to query DBLP and 1 for MAG
dblp_mag_query=1

#number of k-mers of top candidate divided by length of title to perform levenshtein
#should be a float between 0 and 1
levenshteinThreshold=.3

#ratio from levenshtein needed to be considered a match
#should be a float between 0 and 1
ratioThreshold=.85

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



scontrol show hostnames $SLURM_JOB_NODELIST > hostfile.$SLURM_JOBID

parallel --wd $SLURM_SUBMIT_DIR --link --slf hostfile.$SLURM_JOBID -j $SLURM_CPUS_ON_NODE python matchingScript.py --paperLimit {1} --start {2} --end {3} --kmer {4} --repeatingMersRemove {5} --topMersRemove {6} --dblpMagQuery {7} --levenshteinThreshold {8} --ratioThreshold {9} --fileName testing_parallel_matching_script_DBLP_threshold_70 ::: "$total_paper_querying" ::: "${start_values[@]}" ::: "${end_values[@]}" ::: "$k_mer" ::: "$repeating_kmer_remove" ::: "$top_kmer_remove" ::: "$dblp_mag_query" ::: "$levenshteinThreshold" ::: "$ratioThreshold"

echo ""
echo "======================================================"
echo "End Time : $(date)"
echo "======================================================"
