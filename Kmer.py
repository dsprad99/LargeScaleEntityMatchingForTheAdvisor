import matplotlib.pyplot as plt
import sys


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
    arr = mer_builder(title, x)
    for kmer in arr:
        for each_paper in mer_hash[kmer]:
            if each_paper in count:
                count[each_paper] += 1
            else:
                count[each_paper] = 1
    return count


#mer_builder allows for us to build an array of 
#k mers in a given string
#example
#title: hello
#array: mer_array = [hel, elo, llo]

def mer_builder(paper,x):  
    current_mer = ""
    mer_array = []

    if paper is not None:
        for i in range(0, x):
            if i < len(paper):
                current_mer += paper[i]   
        mer_array.append(current_mer)

        while x < len(paper):
            current_mer = current_mer[1:] + paper[x]
            mer_array.append(current_mer)
            x+=1

    return mer_array


#allows us to take in a paper object along with the k-mer represented by x
#in this instance and will build the mer_hash table which will have an ID or 
#ID's associated for every mer
def mer_hashtable(paper, x, mer_hash):
    mer_array = mer_builder(paper.title, x)
    for arr in mer_array:
        if arr not in mer_hash:
            mer_hash[arr] = [paper.paper_id]
        else:
            mer_hash[arr].append(paper.paper_id)



def histogramMers(mer_hash):
        #the 20 on the end will take the 20 most frequent mer values
        top_k_mers = sorted(mer_hash.items(), key=lambda x: len(x[1]), reverse=True)[:20]

        k_mer_labels, k_mer_counts = zip(*[(k, len(v)) for k, v in top_k_mers])

        bar_width = .5
        plt.bar(range(len(k_mer_labels)), k_mer_counts, width=bar_width)
        plt.xticks(range(len(k_mer_labels)), k_mer_labels, rotation=30)
        plt.xlabel("K-mer")
        plt.ylabel("Frequency with hashmap")
        plt.title("Top 20 K-mers Histogram")
        plt.tight_layout()
        plt.show()


def histogramQuery(count_dict):
    # Generate and print the histogram
    top_k_mers = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)[:20]

    k_mer_labels, k_mer_counts = zip(*top_k_mers)

    bar_width = 0.5
    plt.bar(range(len(k_mer_labels)), k_mer_counts, width=bar_width)
    plt.xticks(range(len(k_mer_labels)), k_mer_labels, rotation=90)
    plt.xlabel("DBLP Ids")
    plt.ylabel("Frequency with hashmap")
    plt.title("Top 20 DBLP ID's Histogram")
    plt.tight_layout()
    plt.show()