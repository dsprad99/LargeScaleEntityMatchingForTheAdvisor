import gzip
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


def parse_DBLP_file(file_path, callback, callback2):
    current_paper = None
    with gzip.open(file_path, 'rt', encoding='utf-8') as gz_file:
        count = 0
        for line in gz_file:
            # inproceedings
            if '<article' in line:
                current_paper = Paper()
                current_paper.file_source = "DBLP"
            elif '</article>' in line and current_paper:
                callback2(current_paper)
                if count < 10:
                    callback(current_paper)
                    count += 1

                current_paper = None
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
            paper_identification,doi_num, paper_title = fields[0],fields,[1], fields[4]
            current_paper.paper_id = paper_identification
            current_paper.doi = doi_num
            current_paper.title = paper_title
            current_paper.file_source = "MAG"
            callback2(current_paper)
            if count < 10:
                callback(current_paper)
                count += 1


def print_paper(paper):
    print("Author:", paper.author)
    print("Title:", paper.title)
    print("Paper ID", paper.paper_id)
    print("Year:", paper.year)
    print("Pages:", paper.pages)
    print("URL:", paper.url)
    print()


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



file_path_dblp = 'dblp.xml.gz'
parse_DBLP_file(file_path_dblp, print_paper, counter)

file_path_MAG = 'Papers.txt.gz'
parse_MAG_file(file_path_MAG, print_paper, counter)

print("MAG title count:", mag_title_counter)
print("DBLP title count:", dblp_title_counter)
print("MAG title character count:", mag_title_char_counter)
print("DBLP title character count:", dblp_title_char_counter)
print("Total title count:", mag_title_counter + dblp_title_counter)
print("Total title character count:", mag_title_char_counter + dblp_title_char_counter)























