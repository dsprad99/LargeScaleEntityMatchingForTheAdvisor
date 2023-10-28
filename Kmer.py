import matplotlib.pyplot as plt
import sys


#*Documentation* if when developing the mer_hash table and you 
#pass that you do want it to generate characters in lowercase 
#then when querying you also must pass that you want it to devleop the 
#hash table used to develop in lowercase or you will get an error


#allows us to query a title from our mer_hash that contains
#an ID for every mer that exists
#therefore using the mer_hash it is able to identify the frequency of 
#mers associated with an ID number to find the best candidate
def query_selector(title, mer_hash, x):

    #count = {}
    #for each kmer in querytitle
    # for each paper in hash[kmer]
    #	count[paper] + = 1
    #print count

    count = {}
    arr = mer_builder(title, x, False)
    for kmer in arr:
        try:
            for each_paper in mer_hash[kmer]:
                if each_paper in count:
                    count[each_paper] += 1
                else:
                    count[each_paper] = 1

        except KeyError as e:
            pass
    return count


#purpose of this function is to test how long it takes 
#to query through the DBLP hashtable given MAG titles

#we have a try catch statement in the background that is 
#made to catch any error in the second for loop where if our 
#mer is not in our dblp hash table then we will not get an error
#but it will just pass over it
def query_selector_MAG_test(title, mer_hash, x):

    #count = {}
    #for each kmer in querytitle
    # for each paper in hash[kmer]
    #	count[paper] + = 1
    #print count

    count = {}
    cost=0
    arr = mer_builder(title, x, False)
    for kmer in arr:
        try:
            for each_paper in mer_hash[kmer]:
                cost = cost+1
                if each_paper in count:
                    count[each_paper] += 1
                else:
                    count[each_paper] = 1
        except KeyError as e:
            pass
    print ("matching: ", title, "cost: ", cost, "in ", len(count))
    return count


#mer_builder allows for us to build an array of 
#k mers in a given string
#example
#title: hello
#array: mer_array = [hel, elo, llo]

def mer_builder(paper_title,x, lower_case):  
    if lower_case:
        current_mer = ""
        mer_array = []

        if paper_title is not None:
            for i in range(0, x):
                if i < len(paper_title):
                    current_mer += paper_title[i]   
            mer_array.append(current_mer.lower())

            while x < len(paper_title):
                current_mer = current_mer[1:] + paper_title[x]
                mer_array.append(current_mer.lower())
                x+=1

    else:
        current_mer = ""
        mer_array = []

        if paper_title is not None:
            for i in range(0, x):
                if i < len(paper_title):
                    current_mer += paper_title[i]   
            mer_array.append(current_mer)

            while x < len(paper_title):
                current_mer = current_mer[1:] + paper_title[x]
                mer_array.append(current_mer)
                x+=1

    return mer_array

#allows us to take in a paper object along with the k-mer represented by x
#in this instance and will build the mer_hash table which will have an ID or 
#ID's associated for every mer
def mer_hashtable(paper, x, mer_hash, lower_case):
    mer_array = mer_builder(paper.title, x, lower_case)
    
    for arr in mer_array:
        if arr not in mer_hash:
            mer_hash[arr] = [paper.paper_id]
        else:
            mer_hash[arr].append(paper.paper_id)
    
    


def remove_top_k_mers(mer_hash, k):
        # Sort k-mers by frequency in descending order
        sorted_k_mers = sorted(mer_hash.items(), key=lambda x: len(x[1]), reverse=True)

        # Get the top k k-mers
        top_k_mers = sorted_k_mers[:k]

        # Remove the top k k-mers from the hash table
        for k_mer, papers in top_k_mers:
            del mer_hash[k_mer]

        return mer_hash


def top_candidates(query_dataset,number_of_candidates,k_mer):
    sorted_matches = sorted(query_dataset.items(), key=lambda x: x[1], reverse=True)

    # Print the top 3 matches
    print("Top 3 Matches for using",k_mer,"mer for A Moldable Online Scheduling Algorithm and Its Application to Parallel Short Sequence Mapping.:")
    for i, (paper_id, frequency) in enumerate(sorted_matches[:number_of_candidates], 1):
        print(f"{i}. Paper ID: {paper_id}, Frequency: {frequency}")


#allows us to take in a paper object along with the k-mer represented by x
#in this instance and will build the mer_hash table which will have an ID or 
#ID's associated for every mer
def histogramMers(mer_hash,start_num,end_num, filename=None):
    # Sort k-mers by frequency in descending order
    sorted_k_mers = sorted(mer_hash.items(), key=lambda x: len(x[1]), reverse=True)
    
    # Exclude the top 20 most frequent K-mers
    top_k_mers = sorted_k_mers[start_num:end_num]  # Change the slice as needed

    if not top_k_mers:
        print("No k-mers found in the hash.")
        return

    k_mer_labels, k_mer_counts = zip(*[(k, len(v)) for k, v in top_k_mers])

    bar_width = 0.5
    plt.bar(range(len(k_mer_labels)), k_mer_counts, width=bar_width)
    plt.xticks(range(len(k_mer_labels)), k_mer_labels, rotation=90, fontsize=4)
    plt.xlabel("K-mer")
    plt.ylabel("Frequency with hashmap")
    plt.title("Top 200 K-mers Histogram")
    plt.tight_layout()

    if filename:
        plt.savefig(filename)
    else:
        plt.show()



def histogramQuery(count_dict, filename= None):
    # Generate and print the histogram
    top_k_mers = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)[:3]

    k_mer_labels, k_mer_counts = zip(*top_k_mers)

    bar_width = 0.5
    plt.bar(range(len(k_mer_labels)), k_mer_counts, width=bar_width, color='blue')
    plt.xticks(range(len(k_mer_labels)), k_mer_labels, rotation=90, fontsize=8)  
    plt.xlabel("MAG Ids")
    plt.ylabel("Frequency with hashmap")
    plt.title("Top 3 MAG ID's Histogram")
    plt.tight_layout()

    if filename:
        plt.savefig(filename)
    else:
        plt.show()