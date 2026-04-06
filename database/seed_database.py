# script to initialize the database
# Use a blank ODM database in SQLite
# 2. Load Site, Variable, Method, and Source
# A blank odm database sqlite is used that already has table : preconfigured table
# Run this for only once 
import sqlite3

try:
    # the database should be at your project root
    database_connection = sqlite3.connect("ndvi.sqlite")
    cursor = database_connection.cursor()
    print("Connection successful!")
except sqlite3.Error as e:
    print("Connection failed:", e)

def get_table_info(table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    for column in columns:
        print(column)

# seed the database for site, variable, method and source
class DatabaseSeeder:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def insert_row(self, table, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        print(query)
        self.cursor.execute(query, values)

    def insert_many(self, table, data_list):
        for data in data_list:
            self.insert_row(table, data)
        self.conn.commit()

site_seeder = DatabaseSeeder(database_connection)
site_data = [
    {
        "SiteID": 1,
        "SiteCode": "S001",
        "SiteName": "Logan River",
        "Latitude": 41.735,
        "Longitude": -111.834,
        "State": "UT"
    }
]
# site_seeder.insert_many("sites", site_data)
# source_seeder = DatabaseSeeder(database_connection)
# source_data = [
#     {

#     }
# ]
# get_table_info("variables")
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
        "NoDataValue": -9999
    }
]
variable_seeder = DatabaseSeeder(database_connection)
site_seeder.insert_many("variables", variable_data)

# get_table_info("sources")
# enter the correct value of these items and make PR
source_data = [
    {
        "Organization": "US Geological Survey",
        "SourceDescription": "Water quality monitoring data",
        "SourceLink": "https://waterdata.usgs.gov",
        "ContactName": "test test",
        "Phone": "123123",
        "Email": "testemail@usgs.gov",
        "Address": "test address",
        "City": "Logan",
        "State": "UT",
        "ZipCode": "84321",
        "Citation": "USGS Water Data Repository",
        "MetadataID": 1
    }
]
source_seeder = DatabaseSeeder(database_connection)
site_seeder.insert_many("sources", source_data)

# This could be zero 
get_table_info("methods")