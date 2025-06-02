import pickle
import pandas as pd

df = pd.read_csv("../../matched_urns.csv", dtype={"URN": str}, index_col="URN")
df.index = df.index.astype(str).str.strip()

def open_data(data_file):
    file = open(data_file, 'rb')
    tb_dict = pickle.load(file)
    file.close()

    return tb_dict

def urn_to_name(urn):
    if urn not in df.index:
        return "URN Not Found"
    return f"{df.loc[urn]["Author"]}, {df.loc[urn]["Title"]}"