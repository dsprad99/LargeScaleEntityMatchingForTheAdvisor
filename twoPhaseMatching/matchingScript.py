import argparse
from Parse import parse_MAG_file, parse_DBLP_file,Paper
from matchingProgram import matching_process, build_dblp_hash_table, csv_writer
from thefuzz import process
import time
'''
script to execute matchingProgram used to paper querying
'''

#k value to set for breaking up entities into words
k_value = 8

#Note that DBLP has 6649168 papers set this as the max paper_limit
paper_limit = 200000

#number of top most repeating k-mers within entities themselves (keep this relatively lower)
repeating_mers_remove = 30

#number of top most k-mers to remove
num_removed_kmers = 8000

#number of top candidates from k-mer matching to move on to levenhstein
levenshtein_candidates = 5

results = []

#parsing through data that is being matched, paper you want to start at is stand 
#and end at is end
start = 0
end = 2000000

#threshold for kmers needed to match to move onto levenhstein ratio calculation
#calculated taking matched k-mers/ total number of k-mers
levenshteinThreshold = .4
#threshold to consider candidate a match from levenhstein ratio
ratioThreshold = .85

#if we want to remove already matched candidates
#if we dont want to do this set filter_out_matched to False 
#and you dont need to set matched_file_path either
filter_out_matched = False
#file name that was already matched
matched_file_path = 'mag_to_dblp_query_total_trial1.csv'

#file name that the results will be written to
written_file_name = 'dblpToMagTrial1'

#Options
#DBLP - 1
#MAG - 2
#Citeseer - 3
#to decide which set of data the hashmap is to be built on
hashMap_build_dataset = 1
#used to describe which dataset is being used to query the hashmap
query_dataset = 2


dblp_mer_hash, paper_details, hashmap_build_time = build_dblp_hash_table(hashMap_build_dataset,k_value, paper_limit, repeating_mers_remove,num_removed_kmers,filter_out_matched,matched_file_path)

#Callback that will be called after every iteration of parse_MAG_file and currentPaper will act as the current paper object
#being iterated over
callbacks = [lambda currentPaper: results.extend(matching_process(k_value, dblp_mer_hash, num_removed_kmers,
                                                                  levenshtein_candidates, paper_details,
                                                                  hashmap_build_time, currentPaper,
                                                                  levenshteinThreshold, ratioThreshold,hashMap_build_dataset))]


parse_MAG_file(callbacks, start, end)
csv_writer(results, written_file_name, hashMap_build_dataset, query_dataset)
