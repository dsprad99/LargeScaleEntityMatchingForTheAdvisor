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


def parse_DBLP_file(file_path,callback,count_to,start_paper):
    current_paper = None
    with gzip.open(file_path, 'rt', encoding='utf-8') as gz_file:
        count_line = 0
        pap = []
        i = 0
        current_paper = None
        #help us keep track of if we are inside a paper currently
        inside_paper = False
        for current_line in gz_file:
            if i > count_to:
                break

            if(start_paper<=i):
                #check for closing tag first for cases such as
                #</incollection><incollection mdate="2017-07-12" key="reference/cn/Prinz14" publtype="encyclopedia">
                if '</article>' in current_line or '</inproceedings>' in current_line or '</incollection>' in current_line or '</book>' in current_line:
                    inside_paper = False
                    if current_paper is not None and current_paper.title is not None and current_paper.paper_id is not None:
                        #print("Paper is an Object")
                        #for i in range(len(pap)):
                        #   print(pap[i])
                        for fnction in callback:
                            fnction(current_paper)
                        current_paper = None

                        i+=1

                
                #check for an opening tag to make a new Paper object
                if '<article' in current_line or '<inproceedings' in current_line or '<incollection' in current_line or '<book' in current_line:
                    if not inside_paper:
                        current_paper = Paper()
                        current_paper.file_source = "DBLP"
                        inside_paper = True

                

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

                    pap.append(current_line)
                    count_line += 1

    return i


def parse_MAG_file(callback,start_line, count_to):
    file_path = 'Papers.txt.gz'
    line_counter = 0
    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            line_counter += 1
            if(line_counter > count_to):
                    return
            
            if(start_line <=line_counter):
                line = line.encode('utf-8', errors='replace').decode('utf-8')
                

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
    



