import pandas as pd


def generate_ndvi_data():
    # This function will take csv file of ndvi data from datalogger
    df = pd.read_csv("data_source/ndvi_data.csv", skiprows=[1, 2], na_values=["NAN"])
    df.columns = df.columns.str.strip()
    df = df.fillna(-9999)
    return df
