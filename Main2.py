from time_trial import test_kmer_parameters, csv_writer

def main2():
    #k values we want to try out
    k_values = [3, 4, 5, 6, 7]  
    #kmers that we are removing
    num_removed_kmers = 100
    #limit for the amount of DBLP papers we want to add to our hashmap
    paper_limit = 60000000
    
    #number I will divide into my modulus
    paper_limit_sample = 50000

    #number I want to use as my modulus
    mod = 10000

    csv_writer(test_kmer_parameters(k_values, num_removed_kmers, paper_limit, mod, paper_limit_sample))


if __name__ == "__main__":
    main2()