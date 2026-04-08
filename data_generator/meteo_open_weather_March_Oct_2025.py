# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 10:10:46 2026

@author: A02483178
"""

# -----------------------------
# Setup
# -----------------------------
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from openpyxl import load_workbook

# -----------------------------
# Field configuration
# -----------------------------
FIELD_LAT = 41.97
FIELD_LON = -111.05
FIELD_NAME = "Pelican Lake Northern Utah"
FIELD_ACRES = 45
TIMEZONE = "America/Denver"

# -----------------------------
# Fetch historical weather from Open-Meteo
# -----------------------------
def fetch_weather(lat, lon, start_date, end_date):
    """Fetch hourly historical weather from Open-Meteo"""
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&hourly=temperature_2m,relativehumidity_2m,precipitation,wind_speed_10m"
        f"&timezone={TIMEZONE}"
    )
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Weather API unavailable ({e})")
        return None

start_date = "2025-03-01"
end_date = "2025-10-31"

weather_raw = fetch_weather(FIELD_LAT, FIELD_LON, start_date, end_date)
if not weather_raw:
    raise RuntimeError("Could not fetch weather data!")

print(f"Weather data fetched successfully ({start_date} → {end_date})")

# -----------------------------
# Build hourly DataFrame
# -----------------------------
def build_hourly_dataframe(weather_raw):
    df = pd.DataFrame({
        "LocalDateTime": pd.to_datetime(weather_raw["hourly"]["time"]),
        "temp": weather_raw["hourly"]["temperature_2m"],
        "humidity": weather_raw["hourly"]["relativehumidity_2m"],
        "precip": weather_raw["hourly"]["precipitation"],
        "wind": weather_raw["hourly"]["wind_speed_10m"]
    })
    df["LocalDateTime"] = df["LocalDateTime"].dt.tz_localize(None)  # naive local time
    return df

df_hourly = build_hourly_dataframe(weather_raw)
print(f"Hourly data rows: {len(df_hourly)}")

# -----------------------------
# Aggregate daily
# -----------------------------
def aggregate_daily(df_hourly):
    df_daily = df_hourly.resample('D', on='LocalDateTime').agg(
        temp_max=('temp','max'),
        temp_min=('temp','min'),
        temp_mean=('temp','mean'),
        humidity_mean=('humidity','mean'),
        precip_sum=('precip','sum'),
        wind_mean=('wind','mean')
    ).reset_index()
    df_daily['QualifierCode'] = ""  # optional
    return df_daily

df_daily = aggregate_daily(df_hourly)
print(f"Daily aggregated rows: {len(df_daily)}")

# -----------------------------
# Convert to ODM format
# -----------------------------
def convert_to_odm(df_daily):
    variable_map = {
        "temp_max": 1,
        "temp_min": 2,
        "temp_mean": 3,
        "humidity_mean": 4,
        "precip_sum": 5,
        "wind_mean": 6
    }
    df_long = df_daily.melt(
        id_vars=['LocalDateTime','QualifierCode'],
        value_vars=variable_map.keys(),
        var_name='variableName',
        value_name='Value'
    )
    df_long['variableID'] = df_long['variableName'].map(variable_map)
    df_long['UTCOffset'] = 0  # already naive UTC conversion for Excel
    df_long['DateTimeUTC'] = df_long['LocalDateTime']  # naive UTC for Excel
    return df_long[['LocalDateTime','UTCOffset','DateTimeUTC','variableID','Value','QualifierCode']]

df_odm = convert_to_odm(df_daily)
print("ODM-format conversion done")

# -----------------------------
# Metadata sheet
# -----------------------------
metadata = pd.DataFrame({
    "Field": [
        "LocalDateTime",
        "UTCOffset",
        "DateTimeUTC",
        "variableID",
        "Value",
        "QualifierCode",
        "Units / Notes"
    ],
    "Description": [
        "Local timestamp, naive datetime (UTC), Excel-compatible",
        "Hours offset from UTC (0 here, already naive UTC)",
        "UTC timestamp, naive datetime for Excel",
        "Unique variable ID matching ODM database",
        "Measurement value",
        "Optional quality/flag code",
        (
            "1=temp_max (°F), 2=temp_min (°F), 3=temp_mean (°F), 4=humidity_mean (%), "
            "5=precip_sum (inch), 6=wind_mean (mph)\n\n"
            "Precipitation notes:\n"
            "No precipitation actually occurred – daily sum is 0 if no rain/snow.\n"
            "API hourly resolution – very small hourly values (<0.01 inch) may round to 0.\n"
            "Missing/incomplete hourly data – NaNs may default to 0 when summed.\n"
            "Snow vs Rain – snow may be recorded in mm water equivalent; improper conversion may yield 0."
        )
    ]
})

# -----------------------------
# Save to Excel (safe)
# -----------------------------
excel_file = f"{FIELD_NAME}_weather_daily_odm.xlsx"

try:
    # Try to append Metadata if file exists
    book = load_workbook(excel_file)
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        writer.book = book
        df_odm.to_excel(writer, sheet_name="WeatherData", index=False)
        metadata.to_excel(writer, sheet_name="Metadata", index=False)
        writer.save()
    print(f"ODM-ready Excel updated with Metadata: {excel_file}")
except FileNotFoundError:
    # File does not exist yet, create both sheets
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df_odm.to_excel(writer, sheet_name="WeatherData", index=False)
        metadata.to_excel(writer, sheet_name="Metadata", index=False)
    print(f"ODM-ready Excel saved with Metadata: {excel_file}")