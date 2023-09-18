import gzip
import xml.etree.ElementTree as ET


class Paper:

    def __init__(self):
        self.paper_id = None
        self.author = None
        self.doi = None
        self.year = None
        self.pages = None
        self.title = None
        self.url = None
        self.published_through = None
        self.file_source = None


def parse_DBLP_file(file_path, callback, callback2, callback3,callback4):
    current_paper = None

    with gzip.open(file_path, 'rt', encoding='utf-8') as gz_file:
        count = 0
        for current_line in gz_file:

            if ('</article>' in current_line or '</inproceedings>' in current_line or '</incollection>' in current_line or '</book>' in current_line) and ('<article' in current_line or '<inproceedings' in current_line or '<incollection' in current_line or '<book' in current_line):
                callback(current_paper)
                #callback4(current_paper)
                current_paper = None
                current_paper = Paper()
                callback2(current_paper)
                current_paper.file_source = "DBLP"
                callback3(current_line,current_paper)
          
            elif '<article' in current_line or '<inproceedings' in current_line or '<incollection' in current_line or '<book' in current_line:
                current_paper = Paper()
                callback2(current_paper)
                current_paper.file_source = "DBLP"
                callback3(current_line,current_paper)

            elif '</article>' in current_line or '</inproceedings>' in current_line or '</incollection>' in current_line or '</book>' in current_line:
                callback(current_paper)
                #callback4(current_paper)
                current_paper = None


            if current_paper:
                if '<author>' in current_line:
                    current_paper.author = current_line.replace('<author>', '').replace('</author>', '').strip()
                elif '<year>' in current_line:
                    current_paper.year = current_line.replace('<year>', '').replace('</year>', '').strip()
                elif '<pages>' in current_line:
                    current_paper.pages = current_line.replace('<pages>', '').replace('</pages>', '').strip()
                elif '<title>' in current_line:
                    current_paper.title = current_line.replace('<title>', '').replace('</title>', '').strip()
                elif '<url>' in current_line:
                    current_paper.url = current_line.replace('<url>', '').replace('</url>', '').strip()

        
def parse_MAG_file(file_path, callback, callback2,callback4):
    count = 0
    file_path = 'Papers.txt.gz'
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            fields = line.strip().split('\t')
            current_paper = Paper()
            # field[0] = the paper's MAG ID
            paper_identification, doi_num, paper_title = fields[0], fields[1], fields[4]
            current_paper.paper_id = paper_identification
            current_paper.doi = doi_num
            current_paper.title = paper_title
            current_paper.file_source = "MAG"
            callback2(current_paper)
            callback4(current_paper)
            if count < 10:
                callback(current_paper)
                count += 1


# Callback #1
global print_counter
print_counter = 0

def print_paper(paper):
    global print_counter
    if print_counter < 10:
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
def doi_search(line,paper):
    key_start = line.find('key="') + 5
    key_end = line.find('"', key_start)
    if key_start != -1 and key_end != -1:
        paper.doi = line[key_start:key_end]


#callback 4
global mer_hash
mer_hash = {}

def mer_hashtable(paper):
    x = 3
    current_mer = ""

    if paper.title is not None:
        for i in range(0, x):
            if i < len(paper.title):
                current_mer += paper.title[i]

        while x <= len(paper.title):
            if current_mer not in mer_hash:
                mer_hash[current_mer] = [paper.doi]  
            else:
                mer_hash[current_mer].append(paper.doi)  

            # to test hashmap   
            # print(mer_hash.get(current_mer))

            if x < len(paper.title):
                current_mer = current_mer[1:] + paper.title[x]
            else:
                break
            x += 1




file_path_dblp = 'dblp.xml.gz'
parse_DBLP_file(file_path_dblp, print_paper, counter,doi_search, mer_hashtable)

file_path_MAG = 'Papers.txt.gz'
parse_MAG_file(file_path_MAG, print_paper, counter,mer_hashtable)

print("MAG title count:", mag_title_counter)
print("DBLP title count:", dblp_title_counter)
print("MAG title character count:", mag_title_char_counter)
print("DBLP title character count:", dblp_title_char_counter)
print("Total title count:", mag_title_counter + dblp_title_counter)
print("Total title character count:", mag_title_char_counter + dblp_title_char_counter)



