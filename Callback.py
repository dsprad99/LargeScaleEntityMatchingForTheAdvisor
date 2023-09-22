import matplotlib.pyplot as plt

class Callback:
    def masterCallback(paper, line):
        print_paper(paper)
        counter(paper)
        mag_id_search(line,paper)
        mer_builder(paper)
        

# Callback #1
global print_counter
print_counter = 0

def print_paper(paper):
    global print_counter
    if print_counter < 30:
        if paper is not None:
            print("Author:", paper.author if paper.author else "None")
            print("Title:", paper.title if paper.title else "None")
            print("Paper ID: ", paper.paper_id if paper.paper_id else "None")
            print("Year:", paper.year if paper.year else "None")
            print("Pages:", paper.pages if paper.pages else "None")
            print("URL:", paper.url if paper.url else "None")
            print("DOI:", paper.doi if paper.doi else "None")
            print("Published through:", paper.published_through if paper.published_through else "None")
            print("----------------------------")
        else:
            print("None")
    print_counter += 1



#Callback #2
global dblp_title_counter
global mag_title_counter
global dblp_title_char_counter
global mag_title_char_counter
dblp_title_counter = 0
mag_title_counter = 0
dblp_title_char_counter = 0
mag_title_char_counter = 0
def counter(paper):
    global dblp_title_counter
    global mag_title_counter
    global dblp_title_char_counter
    global mag_title_char_counter

    if paper.title is not None:
        if paper.file_source == "DBLP":
            dblp_title_counter += 1
            dblp_title_char_counter += len(paper.title)
        elif paper.file_source == "MAG":
            mag_title_counter += 1
            mag_title_char_counter += len(paper.title)


#Callback #3
def mag_id_search(line,paper):
    if(paper.file_source== "DBLP"):
        #note: +5 is there to look past the 5 characters (key=") at the start
        key_start = line.find('key="') + 5
        #end is the parenthesis that close the key
        key_end = line.find('"', key_start)
        #if a valid key
        if key_start != -1 and key_end != -1:
            paper.paper_id = line[key_start:key_end]
        


#callback 4
def mer_builder(paper):  
    x = 3
    current_mer = ""
    mer_array = []

    if paper.title is not None:
        for i in range(0, x):
            if i < len(paper.title):
                current_mer += paper.title[i]   
        mer_array.append(current_mer)

        while x < len(paper.title):
            current_mer = current_mer[1:] + paper.title[x]
            mer_array.append(current_mer)
            x+=1

    mer_hashtable(paper, mer_array)



global mer_hash
mer_hash = {}
global hash_counter
hash_counter = 0
def mer_hashtable(paper, mer_array):
    global hash_counter
    # Want the local id as the value
    for arr in mer_array:
        if arr not in mer_hash:
            mer_hash[arr] = [paper.paper_id]
        else:
            mer_hash[arr].append(paper.paper_id)
    
    hash_counter += 1
    if hash_counter <= 10:
        print(mer_hash)
    
    histogramMers(mer_hash, hash_counter)



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

    

