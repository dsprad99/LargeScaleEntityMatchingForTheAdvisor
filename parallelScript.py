from time_trial import csv_writer, average_histogram, build_dblp_hash_table, perform_trials

def perform_and_write_results(k_value, paper_limit, selected_dblp_papers, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details, hashmap_build_time, repeat_kmer_hashmap, repeating_mers_remove, start_paper, end_paper, output_filename):
    results = perform_trials(k_value, end_paper - start_paper, selected_dblp_papers, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details, hashmap_build_time, repeat_kmer_hashmap, repeating_mers_remove, start_paper)
    csv_writer(results, output_filename)

def parallelScript():
    k_value = 3
    paper_limit = 6649168
    print("Paper Limit For Hashtable Set To: ",paper_limit)
    chosen_probability = 0
    repeating_mers_remove = 0
    num_removed_kmers = [0, 10, 20, 50]
    levenshtein_candidates = 10

    dblp_mer_hash, selected_dblp_papers, paper_details, hashmap_build_time, repeat_kmer_hashmap, repeating_mers_remove = build_dblp_hash_table(k_value, paper_limit, chosen_probability, repeating_mers_remove)

    queries = [
        (0, 50000, 'parallel_query1.csv'),
        (50000, 100000, 'parallel_query2.csv'),
        (100000, 150000, 'parallel_query3.csv'),
        (150000, 200000, 'parallel_query4.csv'),
        (200000, 250000, 'parallel_query5.csv'),
    ]

    for start, end, output_filename in queries:
        perform_and_write_results(k_value, paper_limit, selected_dblp_papers, dblp_mer_hash, num_removed_kmers, levenshtein_candidates, paper_details, hashmap_build_time, repeat_kmer_hashmap, repeating_mers_remove, start, end, output_filename)

if __name__ == "__main__":
    parallelScript()
