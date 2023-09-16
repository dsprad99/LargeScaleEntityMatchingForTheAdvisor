import gzip
import xml.etree.ElementTree as ET
import sys

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
        for line in gz_file:
            # inproceedings
    
            if '<article' in line and '</article>' in line:
                callback2(current_paper)
                callback(current_paper)
                callback4(current_paper)
                current_paper = Paper()
                callback3(line,current_paper)
                current_paper.file_source = "DBLP"
            
            elif '<article' in line and '</inproceedings>' in line:
                callback2(current_paper)
                callback(current_paper)
                callback4(current_paper)
                current_paper = Paper()
                callback3(line,current_paper)
                current_paper.file_source = "DBLP"

            elif '<inproceedings' in line and '</article>' in line:
                callback2(current_paper)
                callback(current_paper)
                callback4(current_paper)
                current_paper = Paper()
                callback3(line,current_paper)
                current_paper.file_source = "DBLP"

            elif '<incollection' in line and '</incollection>' in line:
                callback2(current_paper)
                callback(current_paper)
                callback4(current_paper)
                current_paper = Paper()
                callback3(line,current_paper)
                current_paper.file_source = "DBLP"

            elif '<article' in line and '</incollection>' in line:
                callback2(current_paper)
                callback(current_paper)
                callback4(current_paper)
                current_paper = Paper()
                callback3(line,current_paper)
                current_paper.file_source = "DBLP"

            elif '<incollection' in line and '</article>' in line:
                callback2(current_paper)
                callback(current_paper)
                callback4(current_paper)
                current_paper = Paper()
                callback3(line,current_paper)
                current_paper.file_source = "DBLP"

            elif '<inproceedings' in line and '</inproceedings>' in line:
                callback2(current_paper)
                callback(current_paper)
                callback4(current_paper)
                current_paper = Paper()
                callback3(line,current_paper)
                current_paper.file_source = "DBLP"

            elif '<article' in line:
                current_paper = Paper()
                callback3(line,current_paper)
                current_paper.file_source = "DBLP"
            
            elif '</article>' in line and current_paper:
                callback2(current_paper)
                callback(current_paper)
                callback4(current_paper)
                current_paper = Paper()

            elif '<incollection' in line:
                current_paper = Paper()
                callback3(line,current_paper)
                current_paper.file_source = "DBLP"
            
            elif '</incollection>' in line and current_paper:
                callback2(current_paper)
                callback(current_paper)
                callback4(current_paper)
                current_paper = Paper()

            elif '<inproceedings' in line:
                current_paper = Paper()
                callback3(line,current_paper)
                current_paper.file_source = "DBLP"
            
            elif '</inproceedings>' in line and current_paper:
                callback2(current_paper)
                callback(current_paper)
                callback4(current_paper)
                current_paper = Paper()


            elif current_paper:
                if '<author>' in line:
                    current_paper.author = line.replace('<author>', '').replace('</author>', '').strip()
                elif '<year>' in line:
                    current_paper.year = line.replace('<year>', '').replace('</year>', '').strip()
                elif '<pages>' in line:
                    current_paper.pages = line.replace('<pages>', '').replace('</pages>', '').strip()
                elif '<title>' in line:
                    current_paper.title = line.replace('<title>', '').replace('</title>', '').strip()
    
                    

                elif '<url>' in line:
                    current_paper.url = line.replace('<url>', '').replace('</url>', '').strip()




def parse_MAG_file(file_path, callback, callback2):
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
            if count < 10:
                callback(current_paper)
                count += 1



 #Callback #1       
global print_counter
print_counter = 0 
def print_paper(paper):
    global print_counter
    if print_counter < 10:  
        print("Author:", paper.author)
        print("Title:", paper.title)
        print("Paper ID", paper.paper_id)
        print("Year:", paper.year)
        print("Pages:", paper.pages)
        print("URL:", paper.url)
        print("DOI: ", paper.doi)
        print("Published through: ", paper.published_through)
        print()
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


#implement this into parsing
global mer_hash
mer_hash = {}

def mer_hashtable(paper):
    x = 3
    current_mer = ""

    for i in range(0, x):
        if i < len(paper.title):
            current_mer += paper.title[i]

    while x <= len(paper.title):
        if current_mer not in mer_hash:
            mer_hash[current_mer] = [paper.doi]  
        else:
            mer_hash[current_mer].append(paper.doi)  

        #to test hashmap   
        #print(mer_hash.get(current_mer))
        
        if x < len(paper.title):
            current_mer = current_mer[1:] + paper.title[x]
        else:
            break  
        x += 1



file_path_dblp = 'dblp.xml.gz'
parse_DBLP_file(file_path_dblp, print_paper, counter,doi_search, mer_hashtable)

file_path_MAG = 'Papers.txt.gz'
parse_MAG_file(file_path_MAG, print_paper, counter)

print("MAG title count:", mag_title_counter)
print("DBLP title count:", dblp_title_counter)
print("MAG title character count:", mag_title_char_counter)
print("DBLP title character count:", dblp_title_char_counter)
print("Total title count:", mag_title_counter + dblp_title_counter)
print("Total title character count:", mag_title_char_counter + dblp_title_char_counter)























