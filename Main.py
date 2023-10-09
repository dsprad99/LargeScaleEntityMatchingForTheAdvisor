from Callback import print_paper
from Parse import Paper, parse_DBLP_file, parse_MAG_file
from Kmer import query_selector, mer_hashtable, histogramQuery
import os, psutil
process = psutil.Process()


def main():
    #memoryatstart = process.memory_info().rss 
    #print(memoryatstart/1024/1024)

    file_path_dblp = 'dblp.xml.gz'
    file_path_MAG = 'Papers.txt.gz'

    dblp_mer_hash = {}  
    mag_mer_hash = {}

    dblp_callbacks = [
#        lambda current_paper: print_paper(current_paper),
        lambda current_paper: mer_hashtable(current_paper, 3, dblp_mer_hash)
    ]
    parse_DBLP_file(file_path_dblp, dblp_callbacks)

    mag_callbacks = [
        #lambda current_paper: print_paper(current_paper),
        lambda current_paper: mer_hashtable(current_paper, 3, dblp_mer_hash) 
    ]
    #parse_MAG_file(file_path_MAG, mag_callbacks)

    #memoryatend = process.memory_info().rss 
    #print(memoryatend/1024/1024)
    #print((memoryatend-memoryatstart)/1024/1024)

    query_count1 = query_selector("A Combined Symbolic-Empirical Apprach for the Automatic Translation of Compounds", dblp_mer_hash, 3)
    query_count2 = query_selector("Definite Resolution over Constraint Languages", dblp_mer_hash, 3)
    query_count3 = query_selector("LILOG-DB: Database Support for Knowledge-Based Systems", dblp_mer_hash, 3)

    histogramQuery(query_count1)
    #histogramQuery(query_count2)
    #histogramQuery(query_count3)
 

if __name__ == "__main__":
    main()
