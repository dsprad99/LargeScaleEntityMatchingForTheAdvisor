import gzip
import sys

class Paper:

    def __init__(self):
        self.paper_id = None
        self.author = None
        self.booktitle = None
        self.year = None
        self.pages = None
        self.title = None
        self.url = None
        self.published_through = None

        

def parse_paper_attributes(file_path, callback):
    current_paper = None

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
                elif '<booktitle>' in line:
                    current_paper.booktitle = line.replace('<booktitle>', '').replace('</booktitle>', '').strip()
                elif '<year>' in line:
                    current_paper.year = line.replace('<year>', '').replace('</year>', '').strip()
                elif '<pages>' in line:
                    current_paper.pages = line.replace('<pages>', '').replace('</pages>', '').strip()
                elif '<title>' in line:
                    current_paper.title = line.replace('<title>', '').replace('</title>', '').strip()
                elif '<url>' in line:
                    current_paper.url = line.replace('<url>', '').replace('</url>', '').strip()


def parse_MAG_file(file_path, callback):
    # Replace 'Papers.txt.gz' with the actual file path.
    count = 0
    file_path = 'Papers.txt.gz'
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            fields = line.strip().split('\t')
            current_paper = Paper()
            paper_identification, paper_title = fields[0], fields[4]

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
    print("Booktitle:", paper.booktitle)
    print("URL:", paper.url)
    print()

file_path_dblp = 'dblp.xml.gz'
parse_paper_attributes(file_path_dblp, print_paper)

file_path_MAG = 'Papers.txt.gz'
parse_MAG_file(file_path_MAG, print_paper)




















