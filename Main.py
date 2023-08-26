import urllib.request
import gzip
import shutil
import os
import html
from lxml import etree
import networkx as nx

# URLs of the files to download
urls = [
    "https://dblp.org/src/DblpExampleParser.java",
    "https://dblp.org/src/mmdb-2019-04-29.jar",
    "https://dblp.org/xml/release/dblp-2019-04-01.xml.gz",
    "https://dblp.org/xml/release/dblp-2017-08-29.dtd"
]

# Directory to store downloaded files
download_dir = "downloaded_files"
os.makedirs(download_dir, exist_ok=True)

# Download and save files
for url in urls:
    file_name = os.path.join(download_dir, os.path.basename(url))
    urllib.request.urlretrieve(url, file_name)

# Extract the XML file from the gz archive
gz_file_path = os.path.join(download_dir, "dblp-2019-04-01.xml.gz")
xml_file_path = os.path.join(download_dir, "dblp-2019-04-01.xml")

with gzip.open(gz_file_path, "rb") as f_in:
    with open(xml_file_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

# Preprocess the XML data by replacing undefined entities
with open(xml_file_path, "r", encoding="utf-8") as f:
    xml_data = f.read()

preprocessed_xml_data = html.unescape(xml_data)

# Parse the preprocessed XML data using lxml
parser = etree.XMLParser(recover=True)  # Allow parsing with errors
root = etree.fromstring(preprocessed_xml_data.encode("utf-8"), parser=parser)

# Create a directed graph using NetworkX
graph = nx.DiGraph()

# Add nodes (elements) to the graph and store attributes
for element in root.iter():
    if element.tag == "phdthesis":
        title = element.find("title").text
        graph.add_node(title)
        
        author = element.find("author").text if element.find("author") is not None else None
        year = element.find("year").text if element.find("year") is not None else None
        school = element.find("school").text if element.find("school") is not None else None
        
        graph.nodes[title]["author"] = author
        graph.nodes[title]["title"] = title
        graph.nodes[title]["year"] = year
        graph.nodes[title]["school"] = school

# Access attributes of a specific node using its title (node_name)
node_name = "Modell zur Produktion von Online-Hilfen."
author = graph.nodes[node_name]["author"]
title = graph.nodes[node_name]["title"]
year = graph.nodes[node_name]["year"]
school = graph.nodes[node_name]["school"]

print("Author:", author)
print("Title:", title)
print("Year:", year)
print("School:", school)

# ... (rest of the code)


