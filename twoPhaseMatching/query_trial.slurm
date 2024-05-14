#!/bin/bash
#SBATCH --partition=Orion
#SBATCH --job-name=theAdvisor
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=150GB
#SBATCH --time=2:00:00

echo "======================================================"
echo "Start Time : $(date)"
echo "Submit Dir : $SLURM_SUBMIT_DIR"
echo "Job ID/Name : $SLURM_JOBID / $SLURM_JOB_NAME"
echo "Num Tasks : $SLURM_NTASKS total [$SLURM_NNODES nodes @ $SLURM_CPUS_ON_NODE CPUs/node]"
echo "======================================================"
echo ""

cd $SLURM_SUBMIT_DIR

#total amount of papers that our DBLP will build to 6649168
total_paper_querying=6649168

#this is the paper that we will start running our program on
#due to the fact that DBLP is in XML format rather then CSV it 
#is highly suggested if querying DBLP to start with 0 for simplicity and accuracy
start_paper=0

#paper that we will end at
end_paper=50

#note the number of tasks per node is set as the partitions we have
partitions=$SLURM_CPUS_ON_NODE

#values to iterate over
k_mer_values=(7)
repeating_kmer_remove_values=(0)

#kmers that will be removed at each k-mer
top_kmer_remove_values=(50 500 1000 5000)

#set value to 0 query for DBLP and 1 to query for MAG
dblp_mag_query=0

#numbers of k-mers of top candidate divided by length of title being matched to, to perform levenshtein
#should be a float value between 0 and 1
levenshteinThreshold=.7

#ratio from levenshtein needed to be considered a match
#should be a float value between 0 and 1
ratioThreshold=.85

for k_mer in "${k_mer_values[@]}"; do
    for repeating_kmer_remove in "${repeating_kmer_remove_values[@]}"; do
        for top_kmer_remove in "${top_kmer_remove_values[@]}"; do
            
            divided_work=$(( (end_paper - start_paper) / partitions ))

            echo "DBLP Hashtable Size: $total_paper_querying"
            echo "Partitions: $partitions"
            echo "Divided Work/Partition: $divided_work"
            echo "Start Paper: $start_paper"
            echo "End Paper: $end_paper"
            echo "k-mer: $k_mer"
            echo "Repeating k-mer Remove: $repeating_kmer_remove"
            echo "Top k-mer Remove: $top_kmer_remove"
            echo ""

            start_values=()
            end_values=()

            for i in $(seq 0 $((partitions - 1))); do
                start_values+=($((start_paper + divided_work * i)))
                end_values+=($((start_paper + divided_work * (i + 1))))
            done

            end_values[-1]=$end_paper

            parallel --link python matchingScript.py --paperLimit {1} --start {2} --end {3} --kmer {4} --repeatingMersRemove {5} --topMersRemove {6} --dblpMagQuery {7} --levenshteinThreshold {8} --ratioThreshold {9} --fileName testing_parallel_matching_script_threshold_70 ::: "$total_paper_querying" ::: "${start_values[@]}" ::: "${end_values[@]}" ::: "$k_mer" ::: "$repeating_kmer_remove" ::: "$top_kmer_remove" ::: "$dblp_mag_query" ::: "$levenshteinThreshold" ::: "$ratioThreshold"
            echo ""
            echo "======================================================"
            echo "End Time : $(date)"
            echo "======================================================"
        done
    done
done

