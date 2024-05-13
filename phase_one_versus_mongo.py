import json
import random
from Parse import parse_DBLP_file,parse_citeseer
from Kmer import query_selector,mer_hashtable, remove_top_k_mers, mer_builder,top_candidates_levenshtein, paper_details_population,repeating_kmer_study,matched_dblp_id_filter,filter_and_remove_kmers
import os, psutil
process = psutil.Process()
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import matplotlib.pyplot as plt

class Sentence:
    def __init__(self):
        self.incorrect = None
        self.paper_id = None
        self.language = None

def optimized_kmer_trial(k_value, top_mers_remove,optimized_kmer):
    global id_hash_correct 
    id_hash_correct = {}

    def parse_misspelled_correct_json(file_path, callback):
        with open(file_path, 'r', encoding='utf-8') as f:
            i = 0
            for line in f:
                    i+=1
                    data = json.loads(line)
                    sentence = Sentence()
                    sentence.title = data["edits"][0]["tgt"]["text"]
                    sentence.paper_id = i
                    id_hash_correct[sentence.paper_id] = sentence.title
                    for fnction in callback:
                        fnction(sentence)


    def parse_misspelled_incorrect_json(file_path, callback,limit):
        with open(file_path, 'r', encoding='utf-8') as f:
            i = 0
            for line in f:
                if(i<=limit):
                    i+=1
                    data = json.loads(line)
                    sentence = Sentence()
                    sentence.title = data["edits"][0]["src"]["text"]
                    sentence.language = data["edits"][0]["src"]["lang"]
                    sentence.paper_id = i
                    if(sentence.language == 'fra' or sentence.language == 'pol' or sentence.language == 'jpn' or sentence.language == 'rus'):
                        for fnction in callback:
                            fnction(sentence)
                else:
                    return


    def build_misspelling_hashmap(k, repeating_mers_remove, top_mers_remove, mispelled_words_file):
        # create DBLP hashmap
        dblp_mer_hash = {}
        global selected_dblp_papers
        selected_dblp_papers = []
        # used to map paper IDs to their title
        paper_details = {}
        # used to create a hashmap of kmer repeating frequency
        repeat_kmer_hashmap = {}

        #array that holds all of the DBLP ids of papers that have already been matched
        matched_paper_dblp_id_array=[]
        matched_paper_dblp_id_array= matched_dblp_id_filter(None, matched_paper_dblp_id_array,False)
        arr_builder = lambda current_sentence : mer_builder(current_sentence.title, k, False, False)

        misspelled_callbacks = [
            lambda current_sentence: mer_hashtable(current_sentence, dblp_mer_hash, arr_builder,matched_paper_dblp_id_array),
            lambda current_sentence: paper_details_population(current_sentence.paper_id, current_sentence.title, paper_details)]

        parse_misspelled_correct_json(mispelled_words_file, misspelled_callbacks)
        print(f"DBLP hash table built for k={k}")
        dblp_mer_hash = filter_and_remove_kmers(repeat_kmer_hashmap, dblp_mer_hash, repeating_mers_remove)
        dblp_mer_hash = remove_top_k_mers(dblp_mer_hash, top_mers_remove)

        return dblp_mer_hash, paper_details



    successful_candidates= 0
    total_candidates = 0
    def matching_process(k_value, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,candidate):
            global successful_candidates, total_candidates
            trial_results = []

            start_total_time_query = time.perf_counter()

            start_time_query_phase1 = time.perf_counter()
            query_result = query_selector(dblp_mer_hash, mer_builder(candidate.title, k_value, False, False))
            top_matches = top_candidates_levenshtein(query_result, levenshtein_candidates, candidate.title, paper_details)
            correct_paper = id_hash_correct[candidate.paper_id]
            if top_matches:
                best_match_title = top_matches[0][3]
                end_time_query_phase1 = time.perf_counter()

                trial_results.append({"src_text":candidate.title, "tgt_text":correct_paper, "matched_sentence":best_match_title})

            return trial_results


    def misspelled_results_json_writer(results, file_name):
            with open(file_name, "w") as json_file:
                json.dump(results, json_file, indent=4)


    def comparison(fileName):
        with open(fileName, 'r', encoding='utf-8') as file:
            data = json.load(file)
            counter = 0
            for item in data:
                if(item['matched_sentence']==item['tgt_text']):
                    counter += 1


        return counter


    repeating_mers_remove = 10

    #mispelled_words_file = "github-typo.jsonl"
    mispelled_words_file = "github-typo.jsonl"
    dblp_mer_hash, paper_details = build_misspelling_hashmap(k_value, repeating_mers_remove,top_mers_remove,mispelled_words_file)

    results = []
    levenshtein_candidates = 2

    callbacks = [lambda currentSentence: results.extend(matching_process(k_value, dblp_mer_hash, top_mers_remove,
                                                                    levenshtein_candidates, paper_details, currentSentence))]
    parse_misspelled_incorrect_json(mispelled_words_file, callbacks,100000000)
    counter = 0
    for result in results:
        if(result['tgt_text']==result['matched_sentence']):
            counter += 1
    optimized_kmer.append([counter, k_value, top_mers_remove])


    #writing_to_file = "github_matched_results_different_languages_phase1.json"
    #misspelled_results_json_writer(results, writing_to_file)
    #print("Phase 1 Matches: ",comparison(writing_to_file))


optimized_kmer = []
k_value = [6,7,8,9,10]
top_mers_remove = [100,300,500,700,900]
#k = 3
#mers_remove = 200
#optimized_kmer_trial(k, mers_remove,optimized_kmer)
#k_value = [3,4]
#top_mers_remove = [100,300]


for k in k_value:
    for mers_remove in top_mers_remove:
        optimized_kmer_trial(k, mers_remove,optimized_kmer)


heatmap_data = np.zeros((len(set([x[1] for x in optimized_kmer])), len(set([x[2] for x in optimized_kmer]))))
for item in optimized_kmer:
    k_index = item[1] - min([x[1] for x in optimized_kmer])
    mers_index = item[2] // 200 - 1
    heatmap_data[k_index, mers_index] = item[0]

# Plot heatmap
plt.figure(figsize=(10, 6))
plt.imshow(heatmap_data, cmap='winter', interpolation='nearest')

# Add labels
plt.title('Optimized K-mer vs Top K-mers Removed')
plt.xlabel('Top K-mers Removed')
plt.ylabel('K-mer Length')
plt.xticks(np.arange(len(set([x[2] for x in optimized_kmer]))), sorted(set([x[2] for x in optimized_kmer])))
plt.yticks(np.arange(len(set([x[1] for x in optimized_kmer]))), sorted(set([x[1] for x in optimized_kmer])))

# Add values into each square
for i in range(len(heatmap_data)):
    for j in range(len(heatmap_data[0])):
        plt.text(j, i, f'{heatmap_data[i, j]:.0f}', ha='center', va='center', color='white')

# Add color bar
plt.colorbar(label='Count')

plt.show()
