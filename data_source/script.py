import pandas as pd


def generate_ndvi_data():
    # This function will take csv file of ndvi data from datalogger
    df = pd.read_csv("data_source/ndvi.csv", na_values=["NAN"])
    df = df.iloc[:, :5]
    df.columns = df.columns.str.strip()
    df = df.fillna(-9999)
    return df
