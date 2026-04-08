# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 10:47:21 2026

@author: A02483178
"""

# -----------------------------
# Full NDVI Data to ODM Pipeline
# -----------------------------
import pandas as pd

# -----------------------------
# 1. Configuration
# -----------------------------
csv_file = "/content/Replicated Data(Sheet1).csv"             # Input CSV
excel_file = "alfalfa_ndvi_odm.xlsx"  # Output Excel
MISSING_VALUE = -9999                  # Placeholder for missing values in ODM

# ODM variable mapping
variable_map = {
    "ndvi": 7,           # NDVI unitless 0–1
    "battery_pct": 8,    # Battery percentage %
    "lowwave_dn": 9,     # Low-wave solar radiation (Watts/m²)
    "highwave_dn": 10     # High-wave solar radiation (Watts/m²)
}

# -----------------------------
# 2. Load CSV (skip extra header rows)
# -----------------------------
# Skip the first 3 rows: header, units, aggregation
df_raw = pd.read_csv(csv_file, skiprows=3, header=None)

# Assign proper column names
df_raw.columns = ['LocalDateTime','LowWaveDn_Avg','HighWaveDn_Avg','NDVI_Avg','Battery Charge']

# Strip any extra spaces in column names
df_raw.columns = df_raw.columns.str.strip()

# -----------------------------
# 3. Rename columns for ODM
# -----------------------------
df_raw.rename(columns={
    "NDVI_Avg": "ndvi",
    "Battery Charge": "battery_pct",
    "LowWaveDn_Avg": "lowwave_dn",
    "HighWaveDn_Avg": "highwave_dn"
}, inplace=True)

# Convert LocalDateTime to datetime
df_raw['LocalDateTime'] = pd.to_datetime(df_raw['LocalDateTime'], errors='coerce')

# Keep only relevant columns
df_ndvi = df_raw[['LocalDateTime','ndvi','battery_pct','lowwave_dn','highwave_dn']].copy()

# Convert numeric columns
for col in ['ndvi','battery_pct','lowwave_dn','highwave_dn']:
    df_ndvi[col] = pd.to_numeric(df_ndvi[col], errors='coerce')

# -----------------------------
# 4. Convert to long format for ODM
# -----------------------------
df_odm_ndvi = df_ndvi.melt(
    id_vars=["LocalDateTime"],
    value_vars=['ndvi','battery_pct','lowwave_dn','highwave_dn'],
    var_name="variableName",
    value_name="Value"
)

# Map variable IDs
df_odm_ndvi["variableID"] = df_odm_ndvi["variableName"].map(variable_map)

# -----------------------------
# 5. Replace missing values
# -----------------------------
df_odm_ndvi['Value'] = df_odm_ndvi['Value'].fillna(MISSING_VALUE)

# Add ODM-required columns
df_odm_ndvi["UTCOffset"] = 0
df_odm_ndvi["DateTimeUTC"] = df_odm_ndvi["LocalDateTime"]  # naive datetime for Excel
df_odm_ndvi["QualifierCode"] = ""

# Reorder for ODM
df_odm_ndvi = df_odm_ndvi[["LocalDateTime","UTCOffset","DateTimeUTC","variableID","Value","QualifierCode"]]

# -----------------------------
# 6. Metadata sheet
# -----------------------------
metadata_ndvi = pd.DataFrame({
    "Field": [
        "LocalDateTime",
        "UTCOffset",
        "DateTimeUTC",
        "variableID",
        "Value",
        "QualifierCode",
        "Units / Notes",
        "Missing Value"
    ],
    "Description": [
        "Local timestamp, naive datetime (UTC), Excel-compatible",
        "Hours offset from UTC (0 here)",
        "UTC timestamp, naive datetime for Excel",
        "Unique variable ID matching ODM database",
        "Measurement value",
        "Optional quality/flag code",
        (
            "7=NDVI (unitless 0–1), "
            "8=Battery percentage (%), "
            "9=LowWaveDn_Avg (Watts/m²), "
            "10=HighWaveDn_Avg (Watts/m²)"
        ),
        f"Missing or invalid readings replaced with {MISSING_VALUE}"
    ]
})

# -----------------------------
# 7. Save Excel
# -----------------------------
with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
    df_odm_ndvi.to_excel(writer, sheet_name="NDVIData", index=False)
    metadata_ndvi.to_excel(writer, sheet_name="Metadata", index=False)

print(f"ODM-ready NDVI Excel saved: {excel_file}")