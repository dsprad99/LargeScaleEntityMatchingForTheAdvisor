import argparse
from Parse import parse_MAG_file, parse_DBLP_file,Paper
from matchingProgram import matching_process, build_dblp_hash_table
from thefuzz import process
import time
'''
script to execute matchingProgram used to paper querying
'''

#arguements taken in from slurm script 

k_value = 8

pap = Paper
pap.title = "Mini Delay Spreead TEQ Design in Muulticarrier Ssystem"
pap.paper_id = 000

#Note that DBLP has 6649168 papers set this as the max paper_limit
paper_limit = 200000
repeating_mers_remove = 30
num_removed_kmers = 8000
levenshtein_candidates = 3
results = []
start = 0
end = 0
fileName = "testing123"
top_mers_remove = 0
levenshteinThreshold = .4
ratioThreshold = .85
filter_out_matched = False
matched_file_path = 'mag_to_dblp_query_total_trial1.csv'

#Options
#DBLP - 1
#MAG - 2
#Citeseer - 3
#to decide which set of data the hashmap is to be built on
hashMap_build_dataset = 3
#used to describe which dataset is being used to query the hashmap
query_dataset = 3


dblp_mer_hash, paper_details, hashmap_build_time = build_dblp_hash_table(hashMap_build_dataset,k_value, paper_limit, repeating_mers_remove,top_mers_remove,filter_out_matched,matched_file_path)


print(matching_process(k_value, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,pap, levenshteinThreshold, ratioThreshold,hashMap_build_dataset))

#get array of choices to query from
choices = parse_DBLP_file([], 0, paper_limit)
start_time = time.perf_counter()
#start process of querying, pap.title is what we are looking for
process.extractOne(pap.title, choices)
end_time = time.perf_counter()
execution_time = end_time - start_time

print(execution_time)
