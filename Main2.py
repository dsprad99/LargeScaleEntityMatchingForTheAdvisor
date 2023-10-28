from Callback import print_paper
from Parse import Paper, parse_DBLP_file, parse_MAG_file
from Kmer import query_selector,mer_hashtable, histogramQuery,histogramMers,query_selector_MAG_test, remove_top_k_mers,top_candidates
import os, psutil
process = psutil.Process()
import time


def main2():

    file_path_dblp = 'dblp.xml.gz'
    file_path_MAG = 'Papers.txt.gz'

    dblp_mer_hash = {}  

    dblp_callbacks = [
        lambda current_paper: mer_hashtable(current_paper, 6, dblp_mer_hash,lower_case = False)
    ]
    parse_DBLP_file(file_path_dblp, dblp_callbacks,60000000)
    print("DBLP hash table built")



    start = time.time()
    query_DBLP_1 = query_selector("Optimizing the stretch of independent tasks on a cluster: From sequential tasks to moldable tasks.", dblp_mer_hash, 6)
    end = time.time()
    print(end - start)

    top_candidates(query_DBLP_1,3,6)


if __name__ == "__main__":
    main2()