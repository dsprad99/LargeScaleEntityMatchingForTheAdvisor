from Callback import print_paper, seeker
from Parse import parse_MAG_file,parse_DBLP_file
import argparse
import sys

parser = argparse.ArgumentParser(description='Parse through paper.')
parser.add_argument('--paper_title', type=str, help='Paper that we are trying to find in MAG dataset')

#number of papers that we will count to
count_to = 999999999999999999999999

#callbacks is an array of function that will be called everytime a new paper is generated
#this allowing us to process each paper individually

#In this case we are going to print out every paper up to count_to. This allowing 
#us to at the end of parsing every paper print out the attributes that we assign to that paper object.
args = parser.parse_args()
#paperSearching = args.paper_title 

paperSearching = args.paper_title

callbacks = [lambda current_paper: seeker(current_paper, paperSearching)]

print(1)
sys.stdout.flush()

#Now passing in the functions we want to call at every instane a new paper object is created through callback
#all we have to do is pass in the callbacks array and then where we want to start and stop parsing.
parse_MAG_file(callbacks, 0, count_to)

