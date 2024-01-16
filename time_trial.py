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


def build_dblp_hash_table(k, paper_limit, chosen_probability, repeating_mers_remove):
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
        lambda current_paper: random_sample_papers(current_paper.title, current_paper.paper_id, chosen_probability),
        lambda current_paper: paper_details_population(current_paper.paper_id, current_paper.title, paper_details),
        lambda current_paper: repeating_kmer_study(current_paper, repeat_kmer_hashmap, arr_builder)
    ]

    start_time_build_hashmap = time.time()
    file_path_dblp = 'dblp.xml.gz'
    parse_DBLP_file(file_path_dblp, dblp_callbacks,paper_limit,0)
    print(f"DBLP hash table built for k={k}")
    end_time_build_hashmap = time.time()
    hashmap_build_time = end_time_build_hashmap - start_time_build_hashmap
        
    return dblp_mer_hash, selected_dblp_papers, paper_details, hashmap_build_time, repeat_kmer_hashmap, repeating_mers_remove




def perform_trials(k_value, paper_limit, selected_dblp_papers, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,repeat_kmer_hashmap,repeating_mers_remove,start_paper):
        
    results = []
    remove_k_mer_sum = 0


    for j in range(len(num_removed_kmers)):
        dblp_mer_hash = filter_and_remove_kmers(repeat_kmer_hashmap, dblp_mer_hash, repeating_mers_remove)
        trial_results = []
        successful_candidates = 0
        total_random_papers = 0
        total_query_time = 0
        remove_k_mer_sum += num_removed_kmers[j]

        for i in range(len(selected_dblp_papers)):
            start_time_query = time.time()
            query_result = query_selector(selected_dblp_papers[i][1], dblp_mer_hash, mer_builder(selected_dblp_papers[i][1], 3, False, False))
            top_matches = top_candidates_levenshtein(query_result, levenshtein_candidates, selected_dblp_papers[i][1], paper_details)
            end_time_query = time.time()
            query_time = end_time_query - start_time_query
            total_query_time += query_time

            if len(top_matches) >= 2:
                ratio = top_matches[0][1], "-", top_matches[1][1]
                best_match_id = top_matches[0][0]
                second_best_match_id = top_matches[1][0]
                best_match_title = top_matches[0][3]
                second_best_match_title = top_matches[1][3]
            else:
                ratio = 0
                best_match_id = "None"
                second_best_match_id = 0

            try:
                if selected_dblp_papers[i][1] == best_match_title:
                    successful_candidates += 1
                total_random_papers += 1
            except UnboundLocalError:
                print("An UnboundLocalError occurred. 'best_match_id' is not associated with a value.")

            if i == len(selected_dblp_papers) - 1:
                average_success_rate = (successful_candidates / total_random_papers) * 100
                trial_results.append((k_value, remove_k_mer_sum, paper_limit, selected_dblp_papers[i][1], selected_dblp_papers[i][0], best_match_id, second_best_match_id, query_time, ratio, hashmap_build_time, average_success_rate, (total_query_time / len(selected_dblp_papers))))
            else:
                if selected_dblp_papers[i][1] == best_match_title:
                    trial_results.append((k_value, remove_k_mer_sum, paper_limit, selected_dblp_papers[i][1], selected_dblp_papers[i][0], best_match_id, second_best_match_id, query_time, ratio, hashmap_build_time, 'Match', '-'))
                else:
                    trial_results.append((k_value, remove_k_mer_sum, paper_limit, selected_dblp_papers[i][1], selected_dblp_papers[i][0], best_match_id, second_best_match_id, query_time, ratio, hashmap_build_time, 'NOT MATCH', '-'))

        print(f"Query completed for removing top {remove_k_mer_sum} mers")
        results.extend(trial_results)
    return results


    


#record results for each trial so that we can append them later to our results array that keeps track of each trial
global selected_dblp_papers
selected_dblp_papers = []
def random_sample_papers(paper_title,paper_id,chosen_probability):
    global counter
    global selected_dblp_papers
    random_number = random.random()
    if chosen_probability > random_number*100:
            individual_paper = [paper_id, paper_title]
            selected_dblp_papers.append(individual_paper)




def csv_writer(results, file_name):
    # Write results to a CSV file
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['k', 'num_removed_kmers', 'paper_limit', 'paper_title', 'paper_id', 'best_candidate_id', '2nd_best_candidate_id', 'query_time', 'ratio', 'hashmap_build_time','average_success_rate','average_query_time']
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
                'hashmap_build_time': result[9],
                'average_success_rate': result[10],
                'average_query_time': result[11]
            })
        

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



        