import random
from Callback import print_paper
from Parse import Paper, parse_DBLP_file, parse_MAG_file
from Kmer import query_selector,mer_hashtable, histogramQuery,histogramMers,query_selector_MAG_test, remove_top_k_mers,top_candidates
import os, psutil
process = psutil.Process()
import time
import csv


def test_kmer_parameters(k, num_removed_kmers, paper_limit, num_queries):
    #record results in the list to add to our csv file
    results = []
    file_path_dblp = 'dblp.xml.gz'
    #iterate over all our different k mer values we want to try
    for k_value in k:
        #create DBLP hashmap
        dblp_mer_hash = {}
        
        #build the mer_hash table for DBLP
        dblp_callbacks = [
            lambda current_paper: mer_hashtable(current_paper, k_value, dblp_mer_hash, lower_case=False)
        ]
        start_time_build_hashmap = time.time()
        parse_DBLP_file(file_path_dblp, dblp_callbacks, paper_limit)
        end_time_build_hashmap = time.time()
        hashmap_build_time = end_time_build_hashmap-start_time_build_hashmap
        print(f"DBLP hash table built for k={k_value}")
        
        #papers that we will query these are hardcoded for now
        selected_dblp_papers = ["Fast recommendation on bibliographic networks with sparse-matrix ordering and partitioning."
                                ,"Recommendation on Academic Networks using Direction Aware Citation Analysis."
                                ,"Market sentiments and convergence dynamics in decentralized assignment economies."
                                ,"Axiomatizing the Harsanyi solution, the symmetric egalitarian solution and the consistent solution for NTU-games."]
        
        #record results for each trial so that we can append them later to our results array that keeps track of each trial
        trial_results = []
        for paper_title in selected_dblp_papers:
            start_time_query = time.time()
            #return back a hashmap of counts for each paper
            query_result = query_selector(paper_title, dblp_mer_hash, k_value)
            end_time_query = time.time()

            query_time = end_time_query - start_time_query

            #gives us our top two papers back
            top_matches = top_candidates(query_result, 2, k_value)

            #testing for results from top_matches
            #for i in range(len(top_matches)):
             #   print(top_matches[i])
            
            # Calculate the ratio of counts
            if len(top_matches) >= 2:
                ratio = top_matches[0],"-",top_matches[1]
            else:
                ratio = 0
            
            trial_results.append((k_value, num_removed_kmers, paper_limit, num_queries, paper_title, query_time, ratio,hashmap_build_time,query_time))
        
        results.extend(trial_results)

    # Write results to a CSV file
    with open('kmer_evaluation_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['k', 'num_removed_kmers', 'paper_limit', 'num_queries', 'paper_title', 'query_time', 'ratio','hashmap_build_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            writer.writerow({
                'k': result[0],
                'num_removed_kmers': result[1],
                'paper_limit': result[2],
                'num_queries': result[3],
                'paper_title': result[4],
                'query_time': result[5],
                'ratio': result[6],
                'hashmap_build_time': result[7]
            })


def main2():
    #k values we want to try out
    k_values = [3, 4, 5]  
    #kmers that we are removing
    num_removed_kmers = 100
    #limit for the amount of DBLP papers we want to add to our hashmap
    paper_limit = 60000000
    #to be implemented when random queries is implemented to know the amount of random queries to make
    #Note: Not been implemented at this point in time
    num_queries = 10
    
    test_kmer_parameters(k_values, num_removed_kmers, paper_limit, num_queries)


if __name__ == "__main__":
    main2()