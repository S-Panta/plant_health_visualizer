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
site_data = [
    {
        "SiteID": 1,
        "SiteCode": "S001",
        "SiteName": "Logan River",
        "Latitude": 41.735,
        "Longitude": -111.834,
        "State": "UT",
    }
]

seeder.insert_many("sites", site_data)

# enter the correct value of these items and make PR
variable_data = [
    {
        "VariableCode": "NDVI",
        "VariableName": "NDVI",
        "Speciation": "Not Applicable",
        "VariableUnitsID": 1,
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


# # get_table_info("sources")
# # enter the correct value of these items and make PR
# source_data = [
#     {
#         "Organization": "US Geological Survey",
#         "SourceDescription": "Water quality monitoring data",
#         "SourceLink": "https://waterdata.usgs.gov",
#         "ContactName": "test test",
#         "Phone": "123123",
#         "Email": "testemail@usgs.gov",
#         "Address": "test address",
#         "City": "Logan",
#         "State": "UT",
#         "ZipCode": "84321",
#         "Citation": "USGS Water Data Repository",
#         "MetadataID": 1
#     }
# ]
# source_seeder = DatabaseSeeder()
# source_seeder.insert_many("sources", source_data)

# # This could be zero
# get_table_info("methods")
seeder.commit_to_database()
