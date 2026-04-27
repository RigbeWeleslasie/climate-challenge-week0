import pandas as pd
import os

@staticmethod
def load_data():
    countries = ["Ethiopia", "Kenya", "Sudan", "Tanzania", "Nigeria"]
    dfs = []

    for country in countries:
        filepath = f"data/{country.lower()}_clean.csv"
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df["Country"] = country
            df["Date"] = pd.to_datetime(df["Date"])
            dfs.append(df)

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    
    return None