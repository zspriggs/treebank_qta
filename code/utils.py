import pickle
import pandas as pd

df = pd.read_csv("../matched_urns.csv", dtype={"URN": str}, index_col="URN")
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
    return f"{df.loc[urn]["Author"]}, {df.loc[urn]["Title"]}"

#prob move this eventually
def ll_comprehender(results: dict):
    print(f"Your log likelihood value is: {results['log likelihood']}")
    if results['log likelihood'] < 3.8:
        print("This indicates that the result is not statistically significant.")
        return
    elif results['log likelihood'] > 3.84:
        print("This indicates that the result is significant with p < .05")
    
    if results['log ratio'] > 0:
        print("The log ratio is positive, which indicates that text 1 includes this lemma more")
    else:
        print("The log ratio is positive, which indicates that text 1 includes this lemma more")

    #Research & add more log ratio analysis