import argparse
from time_trial import average_histogram, perform_trials
from Parse import parse_MAG_file
from matchingProgram import matching_process, build_dblp_hash_table, csv_writer, successful_candidates, total_candidates

'''
script to execute matchingProgram used to paper querying
'''

#arguements taken in from slurm script 
parser = argparse.ArgumentParser(description='Your script description')
parser.add_argument('--paperLimit', type=int, help='Paper limit for queries')
parser.add_argument('--start', type=int, help='Start value for queries')
parser.add_argument('--end', type=int, help='End value for queries')
parser.add_argument('--fileName', type=str, help='CSV File Name')

args = parser.parse_args()

k_value = 8

#Note that DBLP has 6649168 papers set this as the max paper_limit
paper_limit = args.paperLimit
repeating_mers_remove = 10
num_removed_kmers = 1000
levenshtein_candidates = 10
results = []
start = args.start
end = args.end

dblp_mer_hash, paper_details, hashmap_build_time = build_dblp_hash_table(k_value, paper_limit, repeating_mers_remove)

print(args.start,args.end)

callbacks = [lambda currentPaper: results.extend(matching_process(k_value, dblp_mer_hash, num_removed_kmers,
                                                                  levenshtein_candidates, paper_details,
                                                                  hashmap_build_time, currentPaper.title))]

parse_MAG_file(callbacks, start, end)

newFileName = f"{args.fileName}_{args.start}_{args.end}.csv"

csv_writer(results, newFileName)



    



