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

'''
@brief: used to build hashtable and then begin candidate process through function calls to k-mer
'''

'''
builds hashtable to hour dblp k-mer value and then ids with that k-mer

@param: k - k-mer value being used for hashing

@param: paper_limit - paper value that we want to go up to in building our hashmap around

@param: repeating_mers_remove - number of most frequently repeating k-mers we want removed

@param: top_mers_remove - removes the most frequent k-mer values in hashmap
'''
def build_dblp_hash_table(k, paper_limit, repeating_mers_remove, top_mers_remove):
    # create DBLP hashmap
    dblp_mer_hash = {}
    global selected_dblp_papers
    selected_dblp_papers = []
    # used to map paper IDs to their title
    paper_details = {}
    # used to create a hashmap of kmer repeating frequency
    repeat_kmer_hashmap = {}
    
    arr_builder = lambda current_paper : mer_builder(current_paper.title, k, False, False)

    # build the mer_hash table for DBLP
    dblp_callbacks = [
        lambda current_paper: mer_hashtable(current_paper, dblp_mer_hash, arr_builder),
        lambda current_paper: paper_details_population(current_paper.paper_id, current_paper.title, paper_details),
        lambda current_paper: repeating_kmer_study(current_paper, repeat_kmer_hashmap, arr_builder)
    ]

    start_time_build_hashmap = time.time()
    parse_DBLP_file( dblp_callbacks,0,paper_limit)
    print(f"DBLP hash table built for k={k}")
    end_time_build_hashmap = time.time()
    hashmap_build_time = end_time_build_hashmap - start_time_build_hashmap
    dblp_mer_hash = filter_and_remove_kmers(repeat_kmer_hashmap, dblp_mer_hash, repeating_mers_remove)
    dblp_mer_hash = remove_top_k_mers(dblp_mer_hash, top_mers_remove)
        
    return dblp_mer_hash, paper_details, hashmap_build_time




'''
the candidate matching process taking place 

*note* many of these parameters are for field values for filling in the trial_results array 

@param: k_value - the k-value we use to query

@param: dblp_hash_map - hashmap containing k-mer values and the ids associated with them

@param: num_removed_kmers - value of k-mers removed

@param: levenshtein_candidates - candidates used to move on to be evaluated in levenshtein process
 
@param: paper_details - details containing a papers ID - paper Title

@param: hashmap_build_time - build time of how long it took to build DBLP hashmap

@param: candidateTitle - title of the paper going through the matching process

@param: levenshteinThreshold - threshold that is the perctage of candidate with the most k-mers divided by length of the paper being queried. ie. should be a float b/t 0 and 1

@param: ratioThreshold - threshold that is the levenshtein ratio in order for there to be a match between a candidate and the paper being queried. ie. should be a float b/t 0 and 1
#
'''
successful_candidates= 0
total_candidates = 0
def matching_process(k_value, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,candidateTitle, levenshteinThreshold, ratioThreshold):
        
    global successful_candidates, total_candidates
    trial_results = []
    

    start_total_time_query = time.time()

    start_time_query_phase1 = time.time()
    query_result = query_selector(dblp_mer_hash, mer_builder(candidateTitle, k_value, False, False))
    end_time_query_phase2 = time.time()
    query_time_phase1 = end_time_query_phase2 - start_time_query_phase1

    #extract the highest int value from the values part of the dictionary to give us the highest frequency match
    if(query_result.values()):
        highest_frequency = max(query_result.values())    
    else:
        highest_frequency = 0
        
    start_time_query_phase2 = time.time()

    #if highest frequency k-mer hashing candidate is 60% of the length of the candidate title we will go ahead with levenshtein
    if((highest_frequency/len(candidateTitle))>levenshteinThreshold):
        top_matches = top_candidates_levenshtein(query_result, levenshtein_candidates, candidateTitle, paper_details)
    else:
        #need to at least initialize the value so we don't throw an error below when checking the len of top_matches
        top_matches=[]

    end_time_query_phase2 = time.time()
    query_time_phase2 =  end_time_query_phase2 - start_time_query_phase2
    
    end_total_time_query = time.time()

    query_time_total = end_total_time_query - start_total_time_query

    correctMatch = None

    #here we make sure that we have two candidates to compare and our best candidate has a levenshtein ration of at least .9
    #in the 2d array the indexes are as follows [id, frequency, levenshtein ratio, paper title]
    if len(top_matches) >= 2 and top_matches[0][2]>ratioThreshold:
        ratio = top_matches[0][1], "-", top_matches[1][1]
        best_match_id = top_matches[0][0]
        second_best_match_id = top_matches[1][0]
        best_match_title = top_matches[0][3]
        second_best_match_title = top_matches[1][3]
        correctMatch = True
    else:
        ratio = 0
        best_match_title = "None"
        second_best_match_title = "None"


   
    if correctMatch:
        trial_results.append((k_value, num_removed_kmers, candidateTitle, best_match_title, second_best_match_title, ratio, hashmap_build_time, 'Match',query_time_phase1,query_time_phase2,query_time_total,levenshteinThreshold,ratioThreshold,'citation'))
        successful_candidates +=1 
    else:
        trial_results.append((k_value, num_removed_kmers, candidateTitle, best_match_title, second_best_match_title, ratio, hashmap_build_time, 'Not Match',query_time_phase1,query_time_phase2,query_time_total,levenshteinThreshold,ratioThreshold,'citation'))
    
    total_candidates += 1



    return trial_results





'''
writes to a csv file containing information about matching_process

@param: results - results from our matching_process in an array

@param: file_name - file name that results will write to
'''
def csv_writer(results, file_name):
    # Write results to a CSV file
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['k', 'num_removed_kmers', 'candidate_paper_title', 'best_candidate_paper_title', '2nd_best_candidate_paper_title', 'ratio', 'hashmap_build_time','match','average_query_time_phase1','average_query_time_phase2','average_query_time_total','levenshteinThreshold','ratioThreshold','citation']
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
                'ratio': result[5],
                'hashmap_build_time': result[6],
                'match': result[7],
                'average_query_time_phase1': result[8],
                'average_query_time_phase2': result[9],
                'average_query_time_total': result[10],
                'levenshteinThreshold': result[11],
                'ratioThreshold': result[12],
                'citation': result[13]
            })
    
        
            if(result[7]=="Match"):
                matching_candidates += 1
            total_candidates += 1

        csvfile.write(f"\nMatching percentage: {matching_candidates/total_candidates:.2%}")
        
        print("Candidates with a match :",matching_candidates)
        print("Total candidates :",total_candidates)

        print("Matching percentage: ",matching_candidates/total_candidates)

        
'''
prints histogram of the average accuracy and query time of results from the matching process

@param: fileName - file we want to pass in to have histogram built after, should normally come from csv_writer

@param: average_accuracy_boolean - true if we ant to see accuracy histogram false otherwise

@param: average_query_time_boolean - true if we ant to see query time histogram false otherwise
'''
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



        
