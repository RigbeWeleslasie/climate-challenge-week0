import pandas as pd
import numpy as np

def load_country_data(filepath, country_name):
    """Load and clean a single country CSV file."""
    df = pd.read_csv(filepath)
    df['Country'] = country_name
    df.replace(-999, np.nan, inplace=True)
    df['Date'] = pd.to_datetime(df['YEAR'] * 1000 + df['DOY'], format='%Y%j')
    df['Month'] = df['Date'].dt.month
    df.drop_duplicates(inplace=True)
    return df

def load_all_countries(data_dir):
    """Load and combine all 5 country datasets."""
    countries = {
        'Ethiopia': 'ethiopia.csv',
        'Kenya': 'kenya.csv',
        'Sudan': 'sudan.csv',
        'Tanzania': 'tanzania.csv',
        'Nigeria': 'nigeria.csv'
    }
    dfs = []
    for country, filename in countries.items():
        filepath = f"{data_dir}/{filename}"
        df = load_country_data(filepath, country)
        dfs.append(df)
        print(f"Loaded {country}: {df.shape}")
    combined = pd.concat(dfs, ignore_index=True)
    print(f"Combined dataset: {combined.shape}")
    return combined
