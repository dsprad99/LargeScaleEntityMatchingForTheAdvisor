import gzip
import sys

class Paper:

    def __init__(self):
        self.paper_id = None
        self.author = None
        self.year = None
        self.pages = None
        self.title = None
        self.url = None
        self.published_through = None

        
title_character_counter_DBLP = 0
number_of_titles_DBLP = 0

title_character_counter_MAG = 0
number_of_titles_MAG = 0


def parse_DBLP_file(file_path, callback):
    current_paper = None
    global title_character_counter_DBLP
    global number_of_titles_DBLP
    with gzip.open(file_path, 'rt', encoding='utf-8') as gz_file:
        count = 0
        for line in gz_file:
            if '<article' in line:
                current_paper = Paper()
            elif '</article>' in line and current_paper:

                if count<10:
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
                    title_character_counter_DBLP += len(current_paper.title)
                    number_of_titles_DBLP += 1
                elif '<url>' in line:
                    current_paper.url = line.replace('<url>', '').replace('</url>', '').strip()


def parse_MAG_file(file_path, callback):
    global title_character_counter_MAG
    global number_of_titles_MAG
    count = 0
    file_path = 'Papers.txt.gz'
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            fields = line.strip().split('\t')
            current_paper = Paper()
            paper_identification, paper_title = fields[0], fields[4]

            title_character_counter_MAG += len(fields[4])
            number_of_titles_MAG += 1

            current_paper.paper_id = paper_identification
            current_paper.title = paper_title
            if(count<10):
                callback(current_paper)
                count+=1



def print_paper(paper):
    print("Author:", paper.author)
    print("Title:", paper.title)
    print("Paper ID", paper.paper_id)
    print("Year:", paper.year)
    print("Pages:", paper.pages)
    print("URL:", paper.url)
    print()

file_path_dblp = 'dblp.xml.gz'
parse_DBLP_file(file_path_dblp, print_paper)

file_path_MAG = 'Papers.txt.gz'
parse_MAG_file(file_path_MAG, print_paper)

print()
print("Total characters parsed for DBLP Paper titles ",title_character_counter_DBLP)
print("Total number of paper titles for DBLP ",number_of_titles_DBLP)
print()

print("Total characters parsed for all MAG Paper titles ",title_character_counter_MAG)
print("Total number of paper titles for DBLP ",number_of_titles_MAG)

print()
print("Total characters parsed for all Paper titles ",title_character_counter_DBLP+ title_character_counter_MAG)
print("Total number of paper titles ",number_of_titles_DBLP+number_of_titles_MAG)




















