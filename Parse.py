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


def parse_DBLP_file(file_path,callback):
    current_paper = None
    line_counter = 0  
    with gzip.open(file_path, 'rt', encoding='utf-8') as gz_file:
        for current_line in gz_file:
            if line_counter >= 20000:  
                break
            line_counter += 1
            if ('</article>' in current_line or '</inproceedings>' in current_line or '</incollection>' in current_line or '</book>' in current_line) and ('<article' in current_line or '<inproceedings' in current_line or '<incollection' in current_line or '<book' in current_line):
                for fnction in callback:
                    fnction(current_paper)
                current_paper = None
                current_paper = Paper()
                current_paper.file_source = "DBLP"
          
            elif '<article' in current_line or '<inproceedings' in current_line or '<incollection' in current_line or '<book' in current_line:
                current_paper = Paper()
                current_paper.file_source = "DBLP"

            elif '</article>' in current_line or '</inproceedings>' in current_line or '</incollection>' in current_line or '</book>' in current_line:
                for fnction in callback:
                    fnction(current_paper)
                current_paper = None
            
            if current_paper:
                if '<author>' in current_line:
                    current_paper.author = current_line.replace('<author>', '').replace('</author>', '').strip()
                elif '<year>' in current_line:
                    current_paper.year = current_line.replace('<year>', '').replace('</year>', '').strip()
                elif '<pages>' in current_line:
                    current_paper.pages = current_line.replace('<pages>', '').replace('</pages>', '').strip()
                elif '<ee' in current_line:
                    doi_value = current_line.replace('<ee', '').replace('</ee>', '').strip()
                    doi_value = doi_value.replace('https://doi.org/', '')  
                    current_paper.doi = doi_value 
                elif '<title>' in current_line:
                    current_paper.title = current_line.replace('<title>', '').replace('</title>', '').strip()
                elif '<url>' in current_line:
                    current_paper.url = current_line.replace('<url>', '').replace('</url>', '').strip()
                elif 'key="' in current_line:
                    key_start = current_line.find('key="') + 5
                    #end is the parenthesis that close the key
                    key_end = current_line.find('"', key_start)
                    #if a valid key
                    if key_start != -1 and key_end != -1:
                        current_paper.paper_id = current_line[key_start:key_end]


def parse_MAG_file(file_path,callback):
    file_path = 'Papers.txt.gz'
    line_counter = 0
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            if line_counter >= 20000: 
                break
            line_counter += 1
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
            for fnction in callback:
                    fnction(current_paper)


