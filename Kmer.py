import matplotlib.pyplot as plt
import sys


def query_selector(title, mer_hash,x):
#count = {}
#for each kmer in querytitle
# for each paper in hash[kmer]
#	count[paper] + = 1
#print count
    count = {}
    arr = mer_builder(title,x)
    for kmer in arr:
        for each_paper in mer_hash[kmer]:
            if each_paper in count:
                count[each_paper] += 1
            else:
                count[each_paper] = 1

        
    print(count)



#callback 4
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



global mer_hash
mer_hash = {}
global hash_counter
hash_counter = 0
def mer_hashtable(paper,x):
    global hash_counter
    mer_array = mer_builder(paper.title,x)
    # Want the local id as the value
    for arr in mer_array:
        if arr not in mer_hash:
            mer_hash[arr] = [paper.paper_id]
        else:
            mer_hash[arr].append(paper.paper_id)
    
    hash_counter += 1
    
    #if hash_counter <= 10:
    #   print(mer_hash)
    calculate_memory_usage(mer_hash)
    #histogramMers(mer_hash, hash_counter)



global total_memory_allocated
total_memory_allocated = 0
def calculate_memory_usage(var):
    global total_memory_allocated
    memory_allocated = sys.getsizeof(var)
    total_memory_allocated += memory_allocated

def get_memory_usage():
    return total_memory_allocated



def histogramMers(mer_hash,hash_counter):
    # Generate and print the histogram of the top 20 k-mers from a sampel size of 1000
    if hash_counter == 10000:

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
