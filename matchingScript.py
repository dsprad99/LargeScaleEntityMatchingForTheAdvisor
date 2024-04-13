import argparse
from time_trial import average_histogram, perform_trials
from Parse import parse_MAG_file, parse_DBLP_file
from matchingProgram import matching_process, build_dblp_hash_table, csv_writer, successful_candidates, total_candidates
import sys
import os, psutil
process = psutil.Process()
from hashtableBuild import buildHashTable

'''
script to execute matchingProgram used to paper querying
'''

#arguements taken in from slurm script 
parser = argparse.ArgumentParser(description='Your script description')
parser.add_argument('--paperLimit', type=int, help='Paper limit for queries')
parser.add_argument('--start', type=int, help='Start value for queries')
parser.add_argument('--end', type=int, help='End value for queries')
parser.add_argument('--fileName', type=str, help='CSV File Name')
parser.add_argument('--kmer', type=int, help='K-Mer value being queried')
parser.add_argument('--repeatingMersRemove', type=int, help='Mers repeated multiple times in query removed')
parser.add_argument('--topMersRemove', type=int, help='Top (most frequent) mers removed')
parser.add_argument('--dblpMagQuery', type=int, help='Choose to query DBLP or MAG')
parser.add_argument('--levenshteinThreshold', type=float, help='Choose K-Mer Percentage threshold to perform Levenshtein')
parser.add_argument('--ratioThreshold', type=float, help='Choose Levenshtein ratio threshold to be considered a match')
parser.add_argument('--filter_out_matched',type=bool, help='Boolean value for whether or not to do filtering on already matched papers')
parser.add_argument('--filter_out_file_path',type=str, help='File path for filtering')
parser.add_argument('--hashMap_build_dataset',type=int, help='dataset hashmap will be built on')

args = parser.parse_args()

hashMap_build_dataset = args.hashMap_build_dataset

k_value = args.kmer

#Note that DBLP has 6649168 papers set this as the max paper_limit
paper_limit = args.paperLimit
repeating_mers_remove = args.repeatingMersRemove
top_mers_remove = args.topMersRemove
levenshtein_candidates = 10
results = []
start = args.start
end = args.end
chooseDBLPMag = args.dblpMagQuery
levenshteinThreshold = args.levenshteinThreshold
ratioThreshold = args.ratioThreshold
filter_out_matched = args.filter_out_matched
filter_out_file_path = args.filter_out_file_path

dblp_mer_hash, paper_details, hashmap_build_time = build_dblp_hash_table(hashMap_build_dataset,k_value, paper_limit, repeating_mers_remove,top_mers_remove, filter_out_matched, filter_out_file_path)

print(args.start,args.end)

callbacks = [lambda currentPaper: results.extend(matching_process(k_value, dblp_mer_hash, top_mers_remove,
                                                                  levenshtein_candidates, paper_details,
                                                                  hashmap_build_time, currentPaper,
                                                                  levenshteinThreshold, ratioThreshold,hashMap_build_dataset))]


if(chooseDBLPMag==1):
	parse_DBLP_file(callbacks,start,end)
	newFileName = f"{args.fileName}_dblp_{args.start}_{args.end}_{args.kmer}_{args.topMersRemove}.csv"

elif(chooseDBLPMag==2): 
	parse_MAG_file(callbacks, start, end)
	newFileName = f"{args.fileName}_mag_{args.start}_{args.end}_{args.kmer}_{args.topMersRemove}.csv"

else:
	print("Ivalid value passed to chooseDBLPMag,to query DBLP please choose 0 for DBLP and 1 for MAG.")
	sys.exit(1)

csv_writer(results, newFileName, hashMap_build_dataset, chooseDBLPMag)




    



