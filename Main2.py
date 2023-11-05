from time_trial import test_kmer_parameters, csv_writer

def main2():
    #k values we want to try out
    k_values = [3, 4, 5, 6, 7]  
    #kmers that we are removing
    #num_removed_kmers = 0

    #these add up using the function we have
    #for example if we are passing in [0,20,30,50,400,500,4000]
    #we are really removing [0,20,50,100,500,1000,5000]
    #this helps significantly with run time so the hashmap does not
    #have to rebuilt every single time now we will just subtract
    num_removed_kmers = [0,20,30,50,400,500,4000]
    #limit for the amount of DBLP papers we want to add to our hashmap
    paper_limit = 30000000000
    

    chosen_probability= .04

    csv_writer(test_kmer_parameters(k_values, num_removed_kmers, paper_limit, chosen_probability))

if __name__ == "__main__":
    main2()