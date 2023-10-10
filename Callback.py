
class Callback:
    def masterCallback(paper, line):
        print_paper(paper)
        counter(paper)

# Callback #1
global print_counter
print_counter = 0


#allows program to print paper attributes from passing in a paper object
def print_paper(paper):
    global print_counter
    if print_counter < 30:
        if paper is not None:
            print("Author:", paper.author if paper.author else "None")

            #note that due to a UTF-8 error I have a try catch statement here 
            #inorder to skip the title if there is an error with the unicode however
            #the characters within the title that are parsed will still remain the same what
            #is printed out is the only thing differnt
            try:
                # Encode the title as UTF-8 and decode it
                title = paper.title.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
                print("Title:", title if title else "None")
            except UnicodeEncodeError:
                print("Title: [Unable to display due to encoding error]")
                
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
#able to count number of papers in MAG and DBLP datasets
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







    

