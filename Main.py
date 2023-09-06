import gzip

def printPaper(line):
    #print(line)
    
    #Attributes include
    #<booktitle>
    #<year>
    #<pages>
    #<title>
    #<author>
    #<url>
    #<crossref>
    #<ee>
    #<pages>


    if '<title>' in line:
        title = line.strip().replace('<title>', 'Title: ').replace('</title>', '')
        print(title)
    
    elif '<author>' in line:
        author = line.replace('<author>', 'Author: ').replace('</author>', '')
        print( author)


def listDBLP(file_path, callback):
    count = 0
    with gzip.open(file_path, 'rt') as gz_file:
        for line in gz_file:
            callback(line)

file_path = 'dblp.xml.gz'
listDBLP(file_path, printPaper)








#listDBLP(“filename”, function):
#printPaper(“filename”)

#Def printpaper(paper):
#print(paper.title)
#print(paper.author)







