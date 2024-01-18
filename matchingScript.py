from time_trial import average_histogram, perform_trials
from Parse import parse_MAG_file
from matchingProgram import matching_process,build_dblp_hash_table,csv_writer


k_value = 3
paper_limit = 1000
repeating_mers_remove = 0
num_removed_kmers = 10
levenshtein_candidates = 10
results = []

dblp_mer_hash, paper_details, hashmap_build_time = build_dblp_hash_table(k_value, paper_limit, repeating_mers_remove)

queries = [
        (0, 50),
        (50, 100),
        (100, 150),
        (150, 200),
        (250, 300)
    ]

callbacks = [lambda currentPaper: results.extend(matching_process(k_value, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details,hashmap_build_time,currentPaper.title))]

index = 0
for (start,end) in queries:
    parse_MAG_file(callbacks, start, end)
    index +=1
    print(index)

fileName = "matchingScriptTest.csv"
csv_writer(results,fileName)

    



