import gzip
import xml.etree.ElementTree as ET
from Callback import Callback

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


def parse_DBLP_file(file_path):
    current_paper = None

    with gzip.open(file_path, 'rt', encoding='utf-8') as gz_file:
        for current_line in gz_file:
            if ('</article>' in current_line or '</inproceedings>' in current_line or '</incollection>' in current_line or '</book>' in current_line) and ('<article' in current_line or '<inproceedings' in current_line or '<incollection' in current_line or '<book' in current_line):
                Callback.masterCallback(current_paper,current_line)
                current_paper = None
                current_paper = Paper()
                current_paper.file_source = "DBLP"
          
            elif '<article' in current_line or '<inproceedings' in current_line or '<incollection' in current_line or '<book' in current_line:
                current_paper = Paper()
                current_paper.file_source = "DBLP"

            elif '</article>' in current_line or '</inproceedings>' in current_line or '</incollection>' in current_line or '</book>' in current_line:
                Callback.masterCallback(current_paper,current_line)
                current_paper = None

            if current_paper:
                if '<author>' in current_line:
                    current_paper.author = current_line.replace('<author>', '').replace('</author>', '').strip()
                elif '<year>' in current_line:
                    current_paper.year = current_line.replace('<year>', '').replace('</year>', '').strip()
                elif '<pages>' in current_line:
                    current_paper.pages = current_line.replace('<pages>', '').replace('</pages>', '').strip()
                elif '<ee>' in current_line:
                    doi_value = current_line.replace('<ee>', '').replace('</ee>', '').strip()
                    doi_value = doi_value.replace('https://doi.org/', '')  
                    current_paper.doi = doi_value 
                elif '<title>' in current_line:
                    current_paper.title = current_line.replace('<title>', '').replace('</title>', '').strip()
                elif '<url>' in current_line:
                    current_paper.url = current_line.replace('<url>', '').replace('</url>', '').strip()

        
def parse_MAG_file(file_path):
    file_path = 'Papers.txt.gz'
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            fields = line.strip().split('\t')
            current_paper = Paper()
            # field[0] = the paper's MAG ID
            paper_identification, doi_num, paper_title = fields[0], fields[2], fields[4]
            current_paper.paper_id = paper_identification

            if doi_num is not None:
                current_paper.doi = doi_num
            else:
                current_paper.doi = None

            current_paper.title = paper_title
            current_paper.file_source = "MAG"
            Callback.masterCallback(current_paper, line)


file_path_dblp = 'dblp.xml.gz'
parse_DBLP_file(file_path_dblp)

file_path_MAG = 'Papers.txt.gz'
parse_MAG_file(file_path_MAG)

