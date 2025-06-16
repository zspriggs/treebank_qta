import pickle
import pandas as pd

DATA_FILE = "./data/treebankData"

df = pd.read_csv("./data/matched_urns.csv", dtype={"URN": str}, index_col="URN")
df.index = df.index.astype(str).str.strip()

def open_data(data_file):
    file = open(data_file, 'rb')
    tb_dict = pickle.load(file)
    file.close()

    return tb_dict

def urn_to_name(urn):
    urn = urn.split('.')[0]
    if urn not in df.index:
        return "URN Not Found"
    return f"{df.loc[urn]['Author']}, {df.loc[urn]['Title']}"

#prob move this eventually
'''
def ll_comprehender(results: dict):
    explanation = f"Your log likelihood value is: {results['log likelihood']}\n"
    if results['log likelihood'] < 3.8:
        explanation += "\nThis indicates that the result is not statistically significant."
        return explanation
    elif results['log likelihood'] > 3.84:
        explanation += "\nThis indicates that the result is significant with p < .05"
    
    
    if results['log ratio'] > 0:
        explanation += "\nThe log ratio is positive, which indicates that text 1 uses this lemma more"
    else:
        explanation += "\nThe log ratio is negative, which indicates that text 1 uses this lemma less"

    return explanation
    #Research & add more log ratio analysis '''