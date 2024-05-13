import matplotlib.pyplot as plt
import sys
from Levenshtein import distance,ratio
from Parse import parse_matching_file

'''
@brief: this class is meant to serve where k-mer calculations will take place

@author: Davis Spradling
'''


'''
allows us to query a title from our mer_hash that contains
an ID for every mer that exists
therefore using the mer_hash it is able to identify the frequency of
mers associated with an ID number to find the best candidate

high frequency = good candidate

@param: mer_hash - has a list of papers associated with each kmer value
ie. ["ere"] = [83212,34233,2321] these id numbers being associated with a paper where that k-mer exits

@param: mer_builder_callback - takes in the mer_builder function and is called to form an array of a title broken
into mers
ie. at 3-mer ["hello"] = ["hel","ell","llo"]


@return: count - will return a count of the ids that are the most frequently associated with the title being queried
'''

def query_selector(mer_hash, mer_builder_callback):

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


'''
allows us to add the title of the paper that an ID is associated with

@param: id - id of the paper passed in

@param: title - title of the associated paper passed in

@paper_dictionary - dictonary of where the values are being stored
'''
def paper_details_population(id, title, paper_dictionary):
    paper_dictionary[id] = title




'''
mer_builder helps us actually build an array containing k-mer values
ie. title: hello   array: mer_array = [hel, elo, llo]

@param: paper_title - string value of our paper title

@param: k - mer value used to split paper_title into k-mer array

@param: lower_case - if false will process characters at lower and uppercase if true otherwise

@param: remove_spaces - if false will not remove spaces if true otherwise

@return: mer_array - returns array of broken up k-mer values from title passed in
'''

def mer_builder(paper_title,k, lower_case = False, remove_spaces = False):

    if paper_title is None:
        return []

    mer_array = []
    current_mer = ""
    i = 0
    while len(current_mer) < k and i < len(paper_title):
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


'''
allows us to take in a paper object and build our mer hashtable by adding
those papers k-mer values with there paper ID to the hashmap

ie. "hello" = 786544
ie. "help" = 786545
["hel"] = [786544,786545]
["ell"] = [786544]
["llo"] = [786544]
["elp] = [786545]

@param: paper-paper object passed in containing attirbutes like papert title, ID number, etc.

@param: mer_hash - k-mer hash table being built

@param: mer_builder_call - callback that will split our title into mers

@param: filter_arr - Is an array that holds DBLP paper_ids. If you want to filer out the papers that have already been matched
then the matched_dblp_id_arr definition needs to be run. Else pass in an empty array.
'''
def mer_hashtable(paper, mer_hash, mer_builder_callback, filter_arr):

    if(paper.paper_id not in filter_arr):
        mer_array = mer_builder_callback(paper)

        for arr in mer_array:
            if arr not in mer_hash:
                mer_hash[arr] = [paper.paper_id]
            else:
                mer_hash[arr].append(paper.paper_id)


'''
removes the top numbers of k-mers in the hashmap
main use case it to reduce frequent k-mer querying

@param: mer_hash - hashtable used to store k-mer values with frequency

@param: x - number of top k-mer values we want removed

@return: mer_hash - hashmap with removed k-mers returned
'''
def remove_top_k_mers(mer_hash, x):
        # Sort k-mers by frequency in descending order
        sorted_k_mers = sorted(mer_hash.items(), key=lambda x: len(x[1]), reverse=True)

        # Get the top k k-mers
        top_k_mers = sorted_k_mers[:x]

        # Remove the top k k-mers from the hash table
        for k_mer, _ in top_k_mers:
            del mer_hash[k_mer]
        return mer_hash


'''
returns our top candidates from a hashmap of IDs and frequency of a k-mers from a string

@param: query_dataset - hashmap that we want to query from

@param: number_of_candidates - number of candidates that we want to see matches best

@return: candidates - returns the best candidates in a 2-d array
'''

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




'''
returns our top candidates from a hashmap of IDs and then goes through a levenshtein algorithm
to find the true best cadidate

@param: query_dataset - hashmap that we will be querying from

@param: number_of_candidates - number of candidates we want to perform levenshtein on

@param: query_title - title that we are trying to compare against

@param: paper_details - allows us to grab the paper id associated with the paper title
'''
def top_candidates_levenshtein(query_dataset,number_of_candidates, query_title, paper_details):
    candidates = []

    #sort matches by frequency
    sorted_matches = sorted(query_dataset.items(), key=lambda x: x[1], reverse=True)

    for i, (paper_id, frequency) in enumerate(sorted_matches[:number_of_candidates], 1):
        candidate_title = paper_details.get(paper_id)
        rat = ratio(query_title, candidate_title)
        candidates.append((paper_id, frequency, rat, candidate_title))

    #sort candidates by the Levenshtein ratio
    candidates.sort(key=lambda x: x[2], reverse=True)

    return candidates



'''
allows us to build a histogram of the highest frequency k-mer

@param: mer_hash - hashmap of the k-mer frequency

@param: start_num - number frequency we want to start at plotting

@param: end_num - number frequency we want to stop plotting
'''

def histogramMers(mer_hash,start_num,end_num, filename=None):
    #sort k-mers by frequency in descending order
    sorted_k_mers = sorted(mer_hash.items(), key=lambda x: len(x[1]), reverse=True)

    #include the top start_num to end_num K-mers
    top_k_mers = sorted_k_mers[start_num:end_num]

    if not top_k_mers:
        print("No k-mers found in the hash.")
        return

    k_mer_labels, k_mer_counts = zip(*[(k, len(v)) for k, v in top_k_mers])

    bar_width = 0.5
    plt.bar(range(len(k_mer_labels)), k_mer_counts, width=bar_width)
    plt.xlabel("K-mer")
    plt.ylabel("Frequency with hashmap")
    plt.title("Top 200 3-Mer Histogram - 1,000,000 Papers")
    plt.tight_layout()

    if filename:
        plt.savefig(filename)
    else:
        plt.show()


'''
allows us to build a histogram of the highest frequently repeated k-mer values within a title

ex: "mississippi"
could have - ssi repeating twice

@param: mer_hash - hashmap of the k-mer frequency

@param: start_num - number frequency we want to start at plotting

@param: end_num - number frequency we want to stop plotting
'''
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



'''
creates a histogram of the results of trying to query by the number of hits we get

@param: count_dict - dictionary containing paper candidates  with there frequency of hits to a cetain title being queried
'''
def histogramQuery(count_dict, filename= None):
    # Generate and print the histogram
    top_k_mers = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)[:10]

    k_mer_labels, k_mer_counts = zip(*top_k_mers)

    bar_width = 0.5
    plt.bar(range(len(k_mer_labels)), k_mer_counts, width=bar_width, color='blue')
    plt.xticks(range(len(k_mer_labels)), k_mer_labels, rotation=90, fontsize=8)
    plt.xlabel("DBLP IDs")
    plt.ylabel("Frequency with hashmap")
    plt.title("Top 10 DBLP ID's Histogram")
    plt.tight_layout()

    if filename:
        plt.savefig(filename)
    else:
        plt.show()



'''
allows us to calcualte most frequently repeated k-mer values

@param: paper - paper object used to pass into mer_builder_call

@param: repeat_kmer_hashmap - hashmap passed in to fill the most frequently repeated k-mers

@paramL mer_builder_callback - callback used to build mer array
'''
def repeating_kmer_study(paper,repeat_kmer_hashmap, mer_builder_callback):
    title_repeated_count = {}
    arr = mer_builder_callback(paper)

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



'''
function to find the difference of papers that have already matched and have no matched, this creating a smaller
hashmap to query from and hopefully make the program faster and more accurate

@param: matched_dblp_file - file path for the matched papers

@param: matched_paper_dblp_id_array - array used to hold values of matched DBLP paper IDs

@param: filter_out_matched - will run the program if set true and not if set to false
'''
def matched_dblp_id_filter(matched_dblp_file,matched_paper_dblp_id_array, filter_out_matched):

    if(filter_out_matched):
        matched_callbacks = [
            lambda current_paper: paper_title_paper_id_matching(current_paper, matched_paper_dblp_id_array)
        ]

        #make parse_matching_file to make it so that it can match the MAG-DBLP matching file
        parse_matching_file(matched_dblp_file,matched_callbacks)

    return matched_paper_dblp_id_array



def paper_title_paper_id_matching(current_paper, paper_title_id_array):
    paper_title_id_array.append(current_paper.paper_id)



'''
function to remove most frequent repeating k-mers using repeating_kmer_study returned hashmap

@param: repeat_kmer_hashmap - hashmap returned from repeating_kmer_study containing most frequent repeated k-mers

@param: dblp_hash_map - hashmap with k-mer value and IDs associated with it in it

@return: dblp_hash_map - dblp hash map with deleted repeating k-mers
'''
def filter_and_remove_kmers(repeat_kmer_hashmap,dblp_hash_map, k):

    # Sort k-mers by their count in descending order
    sorted_k_mers = sorted(repeat_kmer_hashmap.items(), key=lambda x: x[1], reverse=True)
    # Get the top k k-mers
    top_k_mers = sorted_k_mers[:k]

    # Remove the top k k-mers from the hash table
    for k_mer, _ in top_k_mers:
        if k_mer in dblp_hash_map:
            del dblp_hash_map[k_mer]

    return dblp_hash_map