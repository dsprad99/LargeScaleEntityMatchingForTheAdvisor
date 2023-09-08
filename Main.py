import gzip

class Paper:

    def __init__(self):
        self.author = None
        self.booktitle = None
        self.year = None
        self.pages = None
        self.title = None
        self.url = None

        

def parse_paper_attributes(file_path, callback):
    current_paper = None

    with gzip.open(file_path, 'rt', encoding='utf-8') as gz_file:
        for line in gz_file:
            if '<article' in line:
                current_paper = Paper()
            elif '</article>' in line and current_paper:
                callback(current_paper)
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


def print_paper(paper):
    print("Author:", paper.author)
    print("Title:", paper.title)
    print("Year:", paper.year)
    print("Pages:", paper.pages)
    print("Booktitle:", paper.booktitle)
    print("URL:", paper.url)
    print()

file_path = 'dblp.xml.gz'
parse_paper_attributes(file_path, print_paper)







