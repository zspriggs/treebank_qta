import pickle
import os
import pandas as pd
import xml.etree.ElementTree as ET
import re

#DATA_FILE = "./data/treebankData"

#have do do this bc of streamlit
this_dir = os.path.dirname(__file__)


#REFACTOR THIS WITH read_csv FUNC
csv_path = os.path.join(this_dir, "data", "matched_urns.csv")
#df = pd.read_csv(csv_path, dtype={"URN": str}, index_col="URN")
#df.index = df.index.astype(str).str.strip()

DATA_FILE = os.path.join(this_dir, "data", "treebankData")

def open_data():
    file = open(DATA_FILE, 'rb')
    tb_dict = pickle.load(file)
    file.close()

    return tb_dict

def read_metadata():
    csv_path = os.path.join(this_dir, "data", "matched_urns.csv")
    return pd.read_csv(csv_path, dtype={"URN": str})

def read_stopwords():
    path = os.path.join(this_dir, "data", "stopwords_greek.txt")
    with open(path, 'r') as f:
        file_content = f.readlines()
        stopwords = []
        for line in file_content:
            if not("#" in line or len(line) == 0 or line.isspace()):
                stopwords.append(line.strip())
        return stopwords
    return None

#converts urns INCLUDING .xml file extension
def urn_to_name(urn):
    urn = urn.split('.')[0]
    df = read_metadata()
    if urn not in df['URN'].values:
        return "URN Not Found"
    
    row = df.loc[df['URN'] == urn].iloc[0]
    return f"{row['Author']}, {row['Title']}"


def extract_text(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    sentences = root.findall('.//sentence')
    lemmas = []
    for sentence in sentences:
        lemmas.extend([word.get('lemma') for word in sentence.findall('.//word') if word.get('lemma')])
    
    return lemmas

def clean_century(century_str):
    try:
        matches = re.findall(r"[0-9]+", century_str)
    except:
        return None
    
    centuries = [int(match) for match in matches]

    if "B.C." in century_str:
        centuries = [-c for c in centuries]

    if len(centuries) == 1:
        return centuries[0]
    elif len(centuries) == 0:
        print("This date didn't work!\n") #some REALLY advanced coding here, fix this later
        return None

    #if it's a range take the middle value
    return round(sum(centuries) / len(centuries))
