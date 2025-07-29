#use this file for test debug etc

import word_analyzer as wa
import detect_grammar as g
import build_tree
import utils
from utils import urn_to_name, extract_text, open_data
import re
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures





def main():
    file = "../xml/0012-001.xml"
    verb = "τεύχω"
    trees = build_tree.build_trees(file)
    #print(trees)
    for tree in trees:
        dos = g.collect_verb_dos(verb, tree[0], tree[1])
        for do in dos:
            print(do.get('form'), do.get('lemma'), do.get('postag'))



            
def real():
    csv_path = "./data/matched_urns.csv"
    df = pd.read_csv(csv_path, dtype={"URN": str})
    
    data_dict = utils.open_data()

    lemma = 'ἀνήρ'
    
    #print(data_dict[df['URN']][lemma])
    
   # print([data_dict[row['URN']].get(lemma, 0) for __, row in df.iterrows()])
        
    df["lemma raw"] = df.apply(lambda row: data_dict[row.URN].get(lemma,0), axis=1)
    df["lemma rel"] = df.apply(lambda row: data_dict[row.URN].get(lemma,0)/data_dict[row.URN].get("TOTAL_WORDS", 1), axis=1)
    
    #print(df["Date"])
    df["clean century"] = df["Date"].apply(clean_century)
    
    print([row["URN"] for __, row in df.iterrows() if row["clean century"] > 21])

    #data_dict[df['URN']].get(lemma, 0)
    
    #df.plot(kind='scatter', x='clean century', y='lemma rel')
   # plt.savefig('test_rel.png')
        
    plot = sns.lineplot(
        data=df,
        x='clean century',
        y='lemma rel',
        errorbar=('ci',95)  # built-in bootstrap CI
    )
    fig = plot.get_figure()
    fig.savefig("out.png") 


    
    


real()

