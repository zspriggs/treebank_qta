import xml.etree.ElementTree as ET
import os
import pickle
import utils

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

def get_data(folder, dest_file):
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


#delete later
def loadData():
    dbfile = open('testPickle', 'rb')    
    db = pickle.load(dbfile)
    for keys in list(db)[:6]:
        print(keys, '=>')
    dbfile.close()

def chi2_singledoc(lemma, short_urn, data_file):
    file = open(data_file, 'rb')    
    tb_dict = pickle.load(file)

    doc_lemma = tb_dict[short_urn][lemma]
    doc_total = tb_dict[short_urn]["TOTAL_WORDS"]

    #be sure to subtract doc_lemma and doc_total bc we want to exclude doc in question from corpus
    corp_lemma = tb_dict["totals"][lemma] - doc_lemma
    corp_total = tb_dict["totals"]["TOTAL_WORDS"] - doc_total

    chi2, p, dof, expected = utils.chi2(doc_lemma, doc_total, corp_lemma, corp_total)
    print(f"{doc_lemma} {doc_total} {corp_lemma} {corp_total}")
    print(f"{chi2} , {p}, {dof}, {expected}")

    return chi2, p, dof, expected

def main():
    data_file = "testPickle"
    get_data("./xml", data_file)

    lemma = "ἀνήρ"
    chi2_singledoc(lemma, "0012-001.xml", data_file)

main()

