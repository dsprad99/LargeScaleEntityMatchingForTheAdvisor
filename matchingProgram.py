import random
from Parse import parse_DBLP_file
from Kmer import query_selector,mer_hashtable, remove_top_k_mers, mer_builder,top_candidates_levenshtein, paper_details_population,repeating_kmer_study,filter_and_remove_kmers
import os, psutil
process = psutil.Process()
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

Parse.DBLP_line_count_freq = 10000

def build_dblp_hash_table(k, paper_limit, repeating_mers_remove):
    # create DBLP hashmap
    dblp_mer_hash = {}
    global selected_dblp_papers
    selected_dblp_papers = []
    # used to map paper IDs to their title
    paper_details = {}
    # used to create a hashmap of kmer repeating frequency
    repeat_kmer_hashmap = {}
    
    arr_builder = lambda current_paper : mer_builder(current_paper.title, 3, False, False)

    # build the mer_hash table for DBLP
    dblp_callbacks = [
        lambda current_paper: mer_hashtable(current_paper, dblp_mer_hash, arr_builder),
        lambda current_paper: paper_details_population(current_paper.paper_id, current_paper.title, paper_details),
        lambda current_paper: repeating_kmer_study(current_paper, repeat_kmer_hashmap, arr_builder)
    ]

    start_time_build_hashmap = time.time()
    file_path_dblp = 'dblp.xml.gz'
    parse_DBLP_file(file_path_dblp, dblp_callbacks,paper_limit,0)
    print(f"DBLP hash table built for k={k}")
    end_time_build_hashmap = time.time()
    hashmap_build_time = end_time_build_hashmap - start_time_build_hashmap
    dblp_mer_hash = filter_and_remove_kmers(repeat_kmer_hashmap, dblp_mer_hash, repeating_mers_remove)
        
    return dblp_mer_hash, paper_details, hashmap_build_time



successful_candidates= 0
total_candidates = 0
def matching_process(k_value, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,candidateTitle):
        
    global successful_candidates, total_candidates
    trial_results = []
    total_random_papers = 0
    total_query_time = 0
    

    start_time_query = time.time()
    query_result = query_selector(candidateTitle, dblp_mer_hash, mer_builder(candidateTitle, 3, False, False))
    top_matches = top_candidates_levenshtein(query_result, levenshtein_candidates, candidateTitle, paper_details)
    end_time_query = time.time()
    query_time = end_time_query - start_time_query
    

    if len(top_matches) >= 2:
        ratio = top_matches[0][1], "-", top_matches[1][1]
        best_match_id = top_matches[0][0]
        second_best_match_id = top_matches[1][0]
        best_match_title = top_matches[0][3]
        second_best_match_title = top_matches[1][3]
    else:
        ratio = 0
        best_match_title = "None"
        second_best_match_title = "None"


   
    if candidateTitle == best_match_title:
        trial_results.append((k_value, num_removed_kmers, candidateTitle, best_match_title, second_best_match_title, query_time, ratio, hashmap_build_time, 'Match',query_time,'citation'))
        successful_candidates +=1 
    else:
        trial_results.append((k_value, num_removed_kmers, candidateTitle, best_match_title, second_best_match_title, query_time, ratio, hashmap_build_time, 'Not Match',query_time,'citation'))
    
    total_candidates += 1



    return trial_results






def csv_writer(results, file_name):
    # Write results to a CSV file
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['k', 'num_removed_kmers', 'candidate_paper_title', 'best_candidate_paper_title', '2nd_best_candidate_paper_title', 'query_time', 'ratio', 'hashmap_build_time','match','query_time','citation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        total_candidates = 0
        matching_candidates = 0

        for result in results:
            writer.writerow({
                'k': result[0],
                'num_removed_kmers': result[1],
                'candidate_paper_title': result[2],
                'best_candidate_paper_title': result[3],
                '2nd_best_candidate_paper_title': result[4],
                'query_time': result[5],
                'ratio': result[6],
                'hashmap_build_time': result[7],
                'match': result[8],
                'query_time': result[9],
                'citation': result[10]
            })
    
        
            if(result[9]=="Match"):
                matching_candidates += 1
            total_candidates += 1

        print("Candidates with a match :",matching_candidates)
        print("Total candidates :",total_candidates)

        print("Matching percentage: ",matching_candidates/total_candidates)

        

def average_histogram(fileName, average_accuracy_boolean, average_query_time_boolean, print_file_name = None):
        df = pd.read_csv(fileName)

        # Convert '-' to NaN for proper numerical computations and filtering
        df['average_success_rate'] = pd.to_numeric(df['average_success_rate'], errors='coerce')
        df['average_query_time'] = pd.to_numeric(df['average_query_time'], errors='coerce')

        # Drop rows where either 'average_success_rate' or 'average_query_time' is NaN
        df.dropna(subset=['average_success_rate', 'average_query_time'], inplace=True)

        # Create a new column combining 'k' and 'num_removed_kmers'
        df['k_num_combination'] = df['k'].astype(str) + "_" + df['num_removed_kmers'].astype(str)

        # Plotting
        if(average_accuracy_boolean and average_query_time_boolean):
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 18))

        elif(average_accuracy_boolean):
            fig, (ax1) = plt.subplots(1, 1, figsize=(18, 18))

        elif(average_query_time_boolean):
            fig, (ax2) = plt.subplots(1, 1, figsize=(18, 18))

        

        # Setting the positions for the bars
        ind = np.arange(len(df['k_num_combination'].unique()))

        # Width of the bars
        width = 0.35

        if average_accuracy_boolean:
            # Plot for Average Success Rate
            bars1 = ax1.bar(ind, df['average_success_rate'], width, color='blue', label='Average Success Rate')
            ax1.set_xlabel('k value and Number of Removed k-mers')
            ax1.set_ylabel('Average Success Rate')
            ax1.set_title('Histogram of Average Success Rate by k value')
            ax1.set_xticks(ind)
            ax1.set_xticklabels(df['k_num_combination'].unique(), rotation=90)
            ax1.legend()

            # Adding the text on the top of each bar in ax1
            for bar in bars1:
                yval = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2.0, yval, round(yval, 2), va='bottom', ha='center')

            if(print_file_name and average_query_time_boolean==False):
                plt.savefig(print_file_name)
            elif(average_query_time_boolean==False):
                plt.show()

        if average_query_time_boolean:
            # Plot for Average Query Time
            bars2 = ax2.bar(ind, df['average_query_time'], width, color='green', label='Average Query Time')
            ax2.set_xlabel('k value and Number of Removed k-mers')
            ax2.set_ylabel('Average Query Time')
            ax2.set_title('Histogram of Average Query Time by k value and Num Removed k-mers')
            ax2.set_xticks(ind)
            ax2.set_xticklabels(df['k_num_combination'].unique(), rotation=90)
            ax2.legend()

            # Adding the text on the top of each bar in ax2 with six decimal places
            for bar in bars2:
                yval = bar.get_height()
                label = "{:.5f}".format(yval)
                ax2.text(bar.get_x() + bar.get_width()/2.0, yval, label, va='bottom', ha='center')

            if(print_file_name and average_accuracy_boolean==False):
                plt.savefig(print_file_name)
            elif(average_accuracy_boolean==False):
                plt.show()

        
        if(print_file_name and average_query_time_boolean and average_accuracy_boolean):
            plt.tight_layout()
            plt.subplots_adjust(hspace=0.5) 
            plt.savefig(print_file_name)
        elif(average_query_time_boolean and average_accuracy_boolean):
            plt.tight_layout()
            plt.subplots_adjust(hspace=0.5) 
            plt.show()



        
