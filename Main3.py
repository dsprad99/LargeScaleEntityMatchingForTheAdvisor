from Callback import print_paper, counter
from Parse import Paper, parse_DBLP_file, parse_MAG_file
from Kmer import query_selector,mer_hashtable, histogramQuery,histogramMers,query_selector_MAG_test, remove_top_k_mers, repeating_kmer_study,histogramRepeatedMers,mer_builder
import os, psutil
process = psutil.Process()
import time


def main3():
    # build the mer_hash table for DBLP
    dblp_callbacks = [
    ]

    file_path_dblp = 'dblp.xml.gz'
    paper_limit = 60000000000000000000000
    print(parse_MAG_file(file_path_dblp, dblp_callbacks,0,paper_limit))
        

    


if __name__ == "__main__":
    main3()