import pandas as pd

def cleaning_df(df):
    unofficial_years = [1906]
    unofficial_sports = ["Alpinism"]

    if "Year" in df.columns:
        df = df[~df["Year"].isin(unofficial_years)]

    if "Sport" in df.columns:
        df = df[~df["Sport"].isin(unofficial_sports)]

    return df


