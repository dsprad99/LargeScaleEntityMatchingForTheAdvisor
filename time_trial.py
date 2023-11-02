import random
from Callback import print_paper
from Parse import Paper, parse_DBLP_file, parse_MAG_file
from Kmer import query_selector,mer_hashtable, histogramQuery,histogramMers,query_selector_MAG_test, remove_top_k_mers,top_candidates
import os, psutil
process = psutil.Process()
import time
import csv

def test_kmer_parameters(k, num_removed_kmers, paper_limit,mod,paper_limit_sample):
    #record results in the list to add to our csv file
    results = []
    file_path_dblp = 'dblp.xml.gz'
    all_trial_results = []
    #iterate over all our different k mer values we want to try
    for k_value in k:
        #create DBLP hashmap
        dblp_mer_hash = {}
        
        #build the mer_hash table for DBLP
        dblp_callbacks = [
            lambda current_paper: mer_hashtable(current_paper, k_value, dblp_mer_hash, lower_case=False),
            lambda current_paper: random_sample_papers(current_paper.title, current_paper.paper_id, mod, paper_limit_sample)
        ]
        start_time_build_hashmap = time.time()
        parse_DBLP_file(file_path_dblp, dblp_callbacks, paper_limit)
        end_time_build_hashmap = time.time()
        hashmap_build_time = end_time_build_hashmap-start_time_build_hashmap
        print(f"DBLP hash table built for k={k_value}")
        
        #papers that we will query these are hardcoded for now
        global selected_dblp_papers
        
        #record results for each trial so that we can append them later to our results array that keeps track of each trial

        #Note: Problem when looping through due to 
        trial_results = []
        for i in range(len(selected_dblp_papers)):
                    start_time_query = time.time()
                    #return back a hashmap of counts for each paper
                    query_result = query_selector(selected_dblp_papers[i][1], dblp_mer_hash, k_value)
                    end_time_query = time.time()

                    query_time = end_time_query - start_time_query

                    #gives us our top two papers back
                    top_matches = top_candidates(query_result, 2)

                    #testing for results from top_matches
                    #for i in range(len(top_matches)):
                    #   print(top_matches[i])
                    
                    # Calculate the ratio of counts
                    if len(top_matches) >= 2:
                        ratio = top_matches[0][1],"-",top_matches[1][1]
                        best_match_id = top_matches[0][0]
                        second_best_match_id = top_matches[1][0]
                    else:
                        ratio = 0
                        best_match_id = "None"
                        second_best_match_id = 0
                    
                    trial_results.append((k_value, num_removed_kmers, paper_limit, selected_dblp_papers[i][1],selected_dblp_papers[i][0],best_match_id,second_best_match_id, query_time, ratio,hashmap_build_time,query_time))
        all_trial_results.extend(trial_results)
    results.extend(all_trial_results)
    return results

    


#record results for each trial so that we can append them later to our results array that keeps track of each trial
global counter
counter = 0
global selected_dblp_papers
selected_dblp_papers = []
def random_sample_papers(paper_title,paper_id,mod,paper_limit_sample):
    global counter
    global selected_dblp_papers
    if counter < paper_limit_sample:
        counter+=1
        if(counter%mod==0):
            individual_paper = [paper_id, paper_title]
            selected_dblp_papers.append(individual_paper)




def csv_writer(results):
    # Write results to a CSV file
    with open('kmer_evaluation_results1.csv', 'w', newline='') as csvfile:
        fieldnames = ['k', 'num_removed_kmers', 'paper_limit', 'paper_title', 'paper_id', 'best_candidate_id', '2nd_best_candidate_id', 'query_time', 'ratio', 'hashmap_build_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            writer.writerow({
                'k': result[0],
                'num_removed_kmers': result[1],
                'paper_limit': result[2],
                'paper_title': result[3],
                'paper_id': result[4],
                'best_candidate_id': result[5],
                '2nd_best_candidate_id': result[6],
                'query_time': result[7],
                'ratio': result[8],
                'hashmap_build_time': result[9]
            })