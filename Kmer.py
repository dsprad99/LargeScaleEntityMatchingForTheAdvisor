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
def query_selector(title, mer_hash, x, mer_builder_callback):

    #count = {}
    #for each kmer in querytitle
    # for each paper in hash[kmer]
    #	count[paper] + = 1
    #print count

    count = {}
    arr = mer_builder_callback
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
def query_selector_MAG_test(title, mer_hash, x, mer_builder_callback):

    #count = {}
    #for each kmer in querytitle
    # for each paper in hash[kmer]
    #	count[paper] + = 1
    #print count

    count = {}
    cost=0
    arr = mer_builder_callback
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

def mer_builder(paper_title,x, lower_case = False, remove_spaces = False):  
    
    if paper_title is None:
        return []

    mer_array = []
    current_mer = ""
    i = 0
    while len(current_mer) < x and i < len(paper_title):
        if remove_spaces and paper_title[i] == ' ':
            i += 1
            continue
        current_mer += paper_title[i]
        i += 1

    if lower_case:
        current_mer = current_mer.lower()
    mer_array.append(current_mer)

    while i < len(paper_title):
        #we will skip the current character value we are on
        #if remove_spaces is true and we have a space
        if remove_spaces and paper_title[i] == ' ':
            i += 1
            continue
        #remove the first character of the current mer
        #and add the next character not in the mer
        current_mer = current_mer[1:] + paper_title[i]
        if lower_case:
            current_mer = current_mer.lower()
        mer_array.append(current_mer)
        i += 1

    return mer_array

#allows us to take in a paper object along with the k-mer represented by x
#in this instance and will build the mer_hash table which will have an ID or 
#ID's associated for every mer
def mer_hashtable(paper, x, mer_hash, lower_case, mer_builder_callback):
    mer_array = mer_builder_callback
    
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
        for k_mer in top_k_mers:
            del mer_hash[k_mer]

        return mer_hash


#returns our top candidates from a hashmap of IDs and frequency of a k-mers from a string
def top_candidates(query_dataset,number_of_candidates):
    candidates = []
    #sort our matches in descending (reverse) order from greatest to least
    sorted_matches = sorted(query_dataset.items(), key=lambda x: x[1], reverse=True)
    #for each papers ID we will add it from greatest to least in our candidates array
    #Note: we can add the paper_ID if we want to at some point using a 2D array

    for i, (paper_id, frequency) in enumerate(sorted_matches[:number_of_candidates], 1):
        #should add the paper_id and frequency of the candidate with the most matches at index 0 all the way to the least
        individual_candidate = [paper_id, frequency]
        candidates.append(individual_candidate)
        
    return candidates    



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


def histogramRepeatedMers(mer_hash, start_num, end_num, filename=None):
    if not isinstance(mer_hash, dict):
        print("mer_hash should be a dictionary")
        return

    # Sort the dictionary items by the values (frequencies) in descending order
    sorted_k_mers = sorted(mer_hash.items(), key=lambda x: x[1], reverse=True)

    # Exclude the top K-mers within the specified range
    top_k_mers = sorted_k_mers[start_num:end_num]

    if not top_k_mers:
        print("No K-mers found in the hash.")
        return

    k_mer_labels, k_mer_counts = zip(*top_k_mers)

    bar_width = 0.5
    plt.bar(range(len(k_mer_labels)), k_mer_counts, width=bar_width)
    plt.xticks(range(len(k_mer_labels)), k_mer_labels, rotation=90, fontsize=9)
    plt.xlabel("K-mer")
    plt.ylabel("Frequency with hashmap")
    plt.title(f"Top {end_num - start_num} Repeated K-mers Histogram")
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




def repeating_kmer_study(repeat_kmer_hashmap, current_paper, mer_builder_callback):
    title_repeated_count = {}
    arr = mer_builder_callback(current_paper)

    for kmer in arr:
        if kmer in title_repeated_count:
            title_repeated_count[kmer] += 1
        else:
            title_repeated_count[kmer] = 1

    for mer in title_repeated_count:
        if title_repeated_count[mer] >= 2:
            #if the mer is not in the hashmap there will also be no value in the hashamp
            #therefore we will make a default value 0 
            repeat_count = repeat_kmer_hashmap.get(mer, 0)
            repeat_kmer_hashmap[mer] = repeat_count + (title_repeated_count[mer] - 1)

