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

args = parser.parse_args()


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

dblp_mer_hash, paper_details, hashmap_build_time = buildHashTable(k_value, paper_limit, repeating_mers_remove,top_mers_remove)

print(args.start,args.end)

callbacks = [lambda currentPaper: results.extend(matching_process(k_value, dblp_mer_hash, top_mers_remove,
                                                                  levenshtein_candidates, paper_details,
                                                                  hashmap_build_time, currentPaper.title,
                                                                  levenshteinThreshold, ratioThreshold))]


if(chooseDBLPMag==0):
	parse_DBLP_file(callbacks,start,end)
	newFileName = f"{args.fileName}_dblp_{args.start}_{args.end}_{args.kmer}_{args.topMersRemove}.csv"

elif(chooseDBLPMag==1): 
	parse_MAG_file(callbacks, start, end)
	newFileName = f"{args.fileName}_mag_{args.start}_{args.end}_{args.kmer}_{args.topMersRemove}.csv"

else:
	print("Ivalid value passed to chooseDBLPMag,to query DBLP please choose 0 for DBLP and 1 for MAG.")
	sys.exit(1)

csv_writer(results, newFileName)




    



