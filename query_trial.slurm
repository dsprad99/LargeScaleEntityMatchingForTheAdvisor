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

# Total amount of papers that our DBLP will build to 6649168
total_paper_querying=6649168

# This is the paper that we will start running our program on
start_paper=200

# Paper that we will end at
end_paper=250

# Note the number of tasks per node is set as the partitions we have
partitions=$SLURM_CPUS_ON_NODE

# Values to iterate over
k_mer_values=(7)
repeating_kmer_remove_values=(0)
top_kmer_remove_values=(50 500 1000 5000)

for k_mer in "${k_mer_values[@]}"; do
    for repeating_kmer_remove in "${repeating_kmer_remove_values[@]}"; do
        for top_kmer_remove in "${top_kmer_remove_values[@]}"; do
            # Calculate other parameters based on these values
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

            parallel --link python matchingScript.py --paperLimit {1} --start {2} --end {3} --kmer {4} --repeatingMersRemove {5} --topMersRemove {6} --fileName testing_parallel_matching_script ::: "$total_paper_querying" ::: "${start_values[@]}" ::: "${end_values[@]}" ::: "$k_mer" ::: "$repeating_kmer_remove" ::: "$top_kmer_remove"
            echo ""
            echo "======================================================"
            echo "End Time : $(date)"
            echo "======================================================"
        done
    done
done

