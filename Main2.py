from time_trial import test_kmer_parameters, csv_writer

def main2():
    #k values we want to try out
    k_values = [3, 4, 5, 6, 7]  
    #kmers that we are removing
    #num_removed_kmers = 0
    num_removed_kmers = [0,20,50,100,500,1000,5000]
    #limit for the amount of DBLP papers we want to add to our hashmap
    paper_limit = 50000
    

    chosen_probability= .00001

    csv_writer(test_kmer_parameters(k_values, num_removed_kmers, paper_limit, chosen_probability))

if __name__ == "__main__":
    main2()