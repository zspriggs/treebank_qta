import xml.etree.ElementTree as ET
import os
import pickle
import utils

#Generates a dictionary of dictionaries with lemma counts for each document
# format => {document: {lemma: count, lemma: count}}

#returns dict of lemmas and counts for a document
def get_lemmas(file, running_dict):
    try:
        tree = ET.parse(file)
    except:
        print(f"Failed to parse {file}. Aborting")
        return None
    root = tree.getroot()

    doc_words = 0
    doc_dict = {}

    #count lemma totals for this document and incr total dict
    for word in root.findall('.//word'):
        lemma = word.get('lemma')
        if lemma in doc_dict:
            doc_dict[lemma] += 1
        else:
            doc_dict[lemma] = 1

        if lemma in running_dict["totals"]:
            running_dict["totals"][lemma] += 1
        else:
            running_dict["totals"][lemma] = 1

        doc_words += 1

    doc_dict["TOTAL_WORDS"] = doc_words
    running_dict["totals"]["TOTAL_WORDS"] += doc_words

    short_urn = file.split('/')[-1]
    running_dict[short_urn] = doc_dict

    return running_dict

#can take a while to run, dep on number of files in folder
def generate_data(folder, dest_file):
    file_list = os.listdir(folder)

    mega_dict = {"totals": {"TOTAL_WORDS": 0}}
    count = 0
    for file in file_list:
        result = get_lemmas(f"{folder}/{file}", mega_dict)
        if result is not None:
            mega_dict = result


        print(f"File {count} counted")
        count += 1

    dbfile = open(dest_file, 'ab')
    # source, destination
    pickle.dump(mega_dict, dbfile)                    
    dbfile.close()

    return

def main():
    data_file = "testPickle"
    #generate_data("./xml", data_file)
    data = utils.open_data(data_file)
    
main()

