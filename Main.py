from Callback import print_paper
from Parse import Paper, parse_DBLP_file, parse_MAG_file
from Kmer import query_selector, mer_hashtable, histogramQuery,histogramMers,query_selector_MAG_test
import os, psutil
process = psutil.Process()
import time


def main():
    #memoryatstart = process.memory_info().rss 
    #print(memoryatstart/1024/1024)

    file_path_dblp = 'dblp.xml.gz'
    file_path_MAG = 'Papers.txt.gz'

    dblp_mer_hash = {}  
    mag_mer_hash = {}

    dblp_callbacks = [
        #lambda current_paper: print_paper(current_paper),
        lambda current_paper: mer_hashtable(current_paper, 3, dblp_mer_hash,lower_case = False)
    ]
    parse_DBLP_file(file_path_dblp, dblp_callbacks,6000000)

    mag_callbacks = [
        #lambda current_paper: print_paper(current_paper),
        lambda current_paper: mer_hashtable(current_paper, 3, mag_mer_hash,lower_case = False),
        lambda current_paper: query_selector_MAG_test(current_paper.title, mag_mer_hash, 3)
    ]
    start = time.time()
    parse_MAG_file(file_path_MAG, mag_callbacks,40000)
    end = time.time()
    print(end - start)

    #memoryatend = process.memory_info().rss 
    #print(memoryatend/1024/1024)
    #print((memoryatend-memoryatstart)/1024/1024)

    #query_count1 = query_selector("A Combined Symbolic-Empirical Apprach for the Automatic Translation of Compounds", dblp_mer_hash, 3)
    #query_count2 = query_selector("Definite Resolution over Constraint Languages", dblp_mer_hash, 3)
    #query_count3 = query_selector("LILOG-DB: Database Support for Knowledge-Based Systems", dblp_mer_hash, 3)
    #start = time.time()
    #query_selector("annotated bibliography on biblical interpretation", mag_mer_hash, 3)
    #end = time.time()
    #print(end - start)

    #histogramQuery(query_count1, filename="query_histogram_DBLP_1.png")
    #histogramQuery(query_count1)
    #histogramQuery(query_count2, filename="query_histogram_DBLP_2.png")
    #histogramQuery(query_count2)
    #histogramQuery(query_count3, filename="query_histogram_DBLP_3.png")

    #histogramMers(dblp_mer_hash, filename="most_frequent_200_mer_DBLP_histogram.png")
    #histogramMers(mag_mer_hash, filename="most_frequent_mer_MAG_histogram.png")


 

if __name__ == "__main__":
    main()
