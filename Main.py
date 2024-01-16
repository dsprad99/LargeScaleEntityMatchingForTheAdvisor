from Callback import print_paper
from Parse import Paper, parse_DBLP_file, parse_MAG_file
from Kmer import query_selector,mer_hashtable, histogramQuery,histogramMers,query_selector_MAG_test, remove_top_k_mers, mer_builder
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

    arr_builder = lambda current_paper : mer_builder(current_paper.title, 3, False, False)
    

    dblp_callbacks = [
        #lambda current_paper: print_paper(current_paper),
        lambda current_paper: mer_hashtable(current_paper, dblp_mer_hash,arr_builder)
    ]
    num_papers = parse_DBLP_file(file_path_dblp, dblp_callbacks,1000000)
    #print(len(dblp_mer_hash.keys()))
    #print("Number of papers in DBLP",num_papers)


    #dblp_mer_hash = remove_top_k_mers(dblp_mer_hash , 1000)
    #start = time.time()
    #parse_MAG_file(file_path_MAG, mag_callbacks,10)
    #end = time.time()
    #print(end - start)

    #memoryatend = process.memory_info().rss 
    #print(memoryatend/1024/1024)
    #print((memoryatend-memoryatstart)/1024/1024)

    query_count1 = query_selector("Modeling Structured Open Worlds in a Database System: The FLL-Approach.", dblp_mer_hash,mer_builder("Modeling Structured Open Worlds in a Database System: The FLL-Approach.", 3, False, False))
    print (query_count1)

    #end = time.time()
    #print(end - start)


    #histogramQuery(query_count1, filename="query_histogram_DBLP_1.svg")
    #histogramQuery(query_count1)
    #histogramQuery(query_count2, filename="query_histogram_DBLP_2.png")
    #histogramQuery(query_count2)
    #histogramQuery(query_count3, filename="query_histogram_DBLP_3.png")

    histogramMers(dblp_mer_hash,0,200, filename="most_frequent_million_mers.svg")
    #histogramMers(mag_mer_hash,1,20, filename="most_frequent_mer_MAG_histogram.png")


if __name__ == "__main__":
    main()
