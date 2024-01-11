from time_trial import test_kmer_parameters, csv_writer, average_histogram,build_dblp_hash_table,perform_trials
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def parallelScript():
 #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    #**These will not change except to affect conditions for all methods**#
    
    #for now we will set this number fairly high to make sure all papers with be put into the hashtable from the DBLP
    paper_limit = 1000000000
    #remove the top 10 most frequent repeating mers
    repeating_mers_remove = 10
    #remove the top 0 most frequent mers
    num_removed_kmers = 0
    #number of candidates that have the most k-mers matching a query are selected to continue on 
    #performing a levenshtein ratio
    levenshtein_candidates= 10
    #probability out of 100 that a paper is selected to be compared
    chosen_probability = .5
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #3-Mer
    k_value = 3
    dblp_mer_hash, selected_dblp_papers, paper_details, hashmap_build_time,repeat_kmer_hashmap,repeating_mers_remove = build_dblp_hash_table(k_value,paper_limit, chosen_probability, repeating_mers_remove)

    #Querying hashtable
    start_paper = 0
    paper_limit = 500000
    perform_trials(k_value, paper_limit, selected_dblp_papers, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,repeat_kmer_hashmap,repeating_mers_remove,start_paper)

    start_paper = 500000
    paper_limit = 1000000
    perform_trials(k_value, paper_limit, selected_dblp_papers, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,repeat_kmer_hashmap,repeating_mers_remove,start_paper)
    
    start_paper = 1000000
    paper_limit = 1500000
    perform_trials(k_value, paper_limit, selected_dblp_papers, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,repeat_kmer_hashmap,repeating_mers_remove,start_paper)

    start_paper = 1000000
    paper_limit = 2000000
    perform_trials(k_value, paper_limit, selected_dblp_papers, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,repeat_kmer_hashmap,repeating_mers_remove,start_paper)


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #4-Mer
    k_value = 4
    dblp_mer_hash, selected_dblp_papers, paper_details, hashmap_build_time,repeat_kmer_hashmap,repeating_mers_remove = build_dblp_hash_table(k_value,paper_limit, chosen_probability, repeating_mers_remove)

    #Querying hashtable
    start_paper = 0
    paper_limit = 500000
    perform_trials(k_value, paper_limit, selected_dblp_papers, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,repeat_kmer_hashmap,repeating_mers_remove,start_paper)

    start_paper = 500000
    paper_limit = 1000000
    perform_trials(k_value, paper_limit, selected_dblp_papers, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,repeat_kmer_hashmap,repeating_mers_remove,start_paper)
    
    start_paper = 1000000
    paper_limit = 1500000
    perform_trials(k_value, paper_limit, selected_dblp_papers, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,repeat_kmer_hashmap,repeating_mers_remove,start_paper)

    start_paper = 1000000
    paper_limit = 2000000
    perform_trials(k_value, paper_limit, selected_dblp_papers, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,repeat_kmer_hashmap,repeating_mers_remove,start_paper)




if __name__ == "__main__":
    parallelScript()