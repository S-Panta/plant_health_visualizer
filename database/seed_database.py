# script to initialize the database
# Use a blank ODM database in SQLite
# 2. Load Site, Variable, Method, and Source
# A blank odm database sqlite is used that already has table : preconfigured table
# Run this for only once
import sqlite3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.connection import DatabaseManager

seeder = DatabaseManager()
# Site code : Code used by organization that collects the data to identify the site 
# other value can be NULL
site_data = [
    {
        "SiteID": 1,
        "SiteCode": "PelicanLake",
        "SiteName": "Pelican Lake Farms",
        "Latitude": 40.192,
        "Longitude": -109.682,
        "State": "UT",
    }
]

seeder.insert_many("sites", site_data)
# ndvi is dimensionless, therefore variable units id: 137
variable_data = [
    {
        "VariableCode": "NDVI",
        "VariableName": "NDVI",
        "Speciation": "Not Applicable",
        "VariableUnitsID": 137,
        "SampleMedium": "Land",
        "ValueType": "Field Observation",
        "IsRegular": 0,
        "TimeSupport": 0.0,
        "TimeUnitsID": 1,
        "DataType": "Continuous",
        "GeneralCategory": "Climate",
        "NoDataValue": -9999,
    }
]

seeder.insert_many("variables", variable_data)


# get_table_info("sources")
# enter the correct value of these items and make PR
source_data = [
    {
        "Organization": "Utah State University",
        "SourceDescription": "NDVI measuring site",
        "ContactName": "Utah State University",
        "City": "Logan",
        "State": "UT",
        "Citation":"Utah State University",
        "MetadataID": 0
    }
]
seeder.insert_many("sources", source_data)

# # This could be zero
# get_table_info("methods")
seeder.commit_to_database()
print("all necessary metadata are injected to database")
