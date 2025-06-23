import pickle
import os
import pandas as pd

DATA_FILE = "./data/treebankData"

#have do do this bc of streamlit
this_dir = os.path.dirname(__file__)

csv_path = os.path.join(this_dir, "data", "matched_urns.csv")
df = pd.read_csv(csv_path, dtype={"URN": str}, index_col="URN")
df.index = df.index.astype(str).str.strip()

DATA_FILE = os.path.join(this_dir, "data", "treebankData")

def open_data():
    file = open(DATA_FILE, 'rb')
    tb_dict = pickle.load(file)
    file.close()

    return tb_dict

def urn_to_name(urn):
    urn = urn.split('.')[0]
    if urn not in df.index:
        return "URN Not Found"
    return f"{df.loc[urn]['Author']}, {df.loc[urn]['Title']}"