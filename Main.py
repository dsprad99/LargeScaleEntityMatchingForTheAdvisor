import urllib.request
import gzip
import shutil
import os
import html
from lxml import etree

# URLs of the files to download
urls = [
    "https://dblp.org/src/DblpExampleParser.java",
    "https://dblp.org/src/mmdb-2019-04-29.jar",
    "https://dblp.org/xml/release/dblp-2019-04-01.xml.gz",
    "https://dblp.org/xml/release/dblp-2017-08-29.dtd"
]

# directory stores downloaded files
download_dir = "downloaded_files"
os.makedirs(download_dir, exist_ok=True)

# download/ save files
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

# Find the last 4 elements in the XML tree
last_elements = []
for element in root.iter():
    last_elements.append(element)
    if len(last_elements) == 20:
        break

# Print attributes of the last 4 elements
if last_elements:
    print("Attributes of the last 20 elements:")
    for last_element in last_elements:
        print(f"Element: {last_element.tag}")
        for attr_name, attr_value in last_element.attrib.items():
            print(f"  {attr_name}: {attr_value}")
else:
    print("No elements found in the XML.")


