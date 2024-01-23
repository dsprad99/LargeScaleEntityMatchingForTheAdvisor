from time_trial import average_histogram, perform_trials
from Parse import parse_MAG_file
from matchingProgram import matching_process,build_dblp_hash_table,csv_writer,successful_candidates,total_candidates


k_value = 3
paper_limit = 100000000000000
repeating_mers_remove = 0
num_removed_kmers = 0
levenshtein_candidates = 10
results = []


dblp_mer_hash, paper_details, hashmap_build_time = build_dblp_hash_table(k_value, paper_limit, repeating_mers_remove)

queries = [
        (0, 5),
        (6, 10),
        (11, 15),
        (16, 20),
        (21, 25)
    ]

callbacks = [lambda currentPaper: results.extend(matching_process(k_value, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,currentPaper.title))]

index = 0
for (start,end) in queries:
    parse_MAG_file(callbacks, start, end)
    

fileName = "matchingScriptTest.csv"
csv_writer(results,fileName)


    



