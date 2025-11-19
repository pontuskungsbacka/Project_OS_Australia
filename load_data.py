from pathlib import Path
import pandas as pd
import hashlib as hl

data_dir = Path("data")

def load_olympics_data():
    athletes = pd.read_csv(data_dir / "athlete_events.csv")
    regions = pd.read_csv(data_dir / "noc_regions.csv")

    #anonymisering 
    athletes["Name"] = athletes["Name"].astype(str)
    hashes = athletes["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())
    athletes.insert(1, "Hash values", hashes)
    athletes.drop(columns=["Name"], inplace=True)

    merged = pd.merge(athletes, regions, on="NOC", how="outer")
    return merged

"""
TODO, addera filter för 1906 års tävling samt sporten Alpinism

def cleaning_df(df):
    unofficial_years = [1906]
    unofficial_sports = ["Alpinism"]

    if "Year" in df.columns:
        df = df[~df["Year"].isin(unofficial_years)]

    if "Sport" in df.columns:
        df = df[~df["Sport"].isin(unofficial_sports)]

    return df
    """