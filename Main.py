import xml.etree.ElementTree as ET
from Callback import print_paper
from Parse import Paper, parse_DBLP_file, parse_MAG_file
from Kmer import query_selector, get_memory_usage, mer_hash, mer_hashtable


def main():
    file_path_dblp = 'dblp.xml.gz'
    file_path_MAG = 'Papers.txt.gz'

    dblp_callbacks = [
        lambda current_paper: print_paper(current_paper),
        lambda current_paper: mer_hashtable(current_paper, 3)  
    ]
    #parse_DBLP_file(file_path_dblp, dblp_callbacks)

    mag_callbacks = [
        #lambda current_paper: print_paper(current_paper),
        lambda current_paper: mer_hashtable(current_paper, 3)  
    ]
    parse_MAG_file(file_path_MAG, mag_callbacks)

  
    print("Total Memory Allocated:", get_memory_usage())
    

if __name__ == "__main__":
    main()
