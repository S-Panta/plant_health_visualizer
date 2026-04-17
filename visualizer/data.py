# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 16:36:41 2026

@author: A02483178

data.py
This file handles database access only. Separating data logic from layout
 and callbacks is a good practice because it makes our app easier to debug
 and reuse.
"""

import os
import sqlite3
import pandas as pd

DB_PATH = r"C:\Users\A02483178\OneDrive - USU\Documents\GitHub\plant_health_visualizer\ndvi.sqlite"
TABLE_NAME = "datavalues"

def fetch_data():
    print("Using DB_PATH:", DB_PATH)
    print("Exists?", os.path.exists(DB_PATH))

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)

    query = f"""
        SELECT DateTimeUTC, DataValue
        FROM {TABLE_NAME}
        WHERE DataValue IS NOT NULL
          AND DataValue != -9999
        ORDER BY DateTimeUTC
    """

    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()

    df["DateTimeUTC"] = pd.to_datetime(df["DateTimeUTC"], errors="coerce")
    df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")
    df = df.dropna(subset=["DateTimeUTC", "DataValue"]).reset_index(drop=True)

    df["DateTimeUTC"] = df["DateTimeUTC"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["DataValue"] = df["DataValue"].astype(float)

    return df