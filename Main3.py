from Callback import print_paper
from Parse import Paper, parse_DBLP_file, parse_MAG_file
from Kmer import query_selector,mer_hashtable, histogramQuery,histogramMers,query_selector_MAG_test, remove_top_k_mers, repeating_kmer_study,histogramRepeatedMers,mer_builder
import os, psutil
process = psutil.Process()
import time


def main3():
    #memoryatstart = process.memory_info().rss 
    #print(memoryatstart/1024/1024)

    file_path_dblp = 'dblp.xml.gz'

    repeat_kmer_hashmap = {}

    arr_builder = lambda current_paper : mer_builder(current_paper.title, 3, False, True)


    dblp_callbacks = [
        #lambda current_paper: print_paper(current_paper),
        #lambda current_paper: mer_hashtable(current_paper, 3, dblp_mer_hash,lower_case = False)
        lambda current_paper: repeating_kmer_study(repeat_kmer_hashmap,current_paper,arr_builder)
    ]
    num_papers = parse_DBLP_file(file_path_dblp, dblp_callbacks,1000000)
    #print(len(dblp_mer_hash.keys()))
    #print("Number of repeated mers:",repeat_kmer_hashmap)

    histogramRepeatedMers(repeat_kmer_hashmap,0,20, 'top_repeated_kmers_1000000_spaces_removed.png')


if __name__ == "__main__":
    main3()