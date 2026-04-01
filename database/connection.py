# script to initialize the database
# Use a blank ODM database in SQLite
# 2. Load Site, Variable, Method, and Source
# A blank odm database sqlite is used that already has table : preconfigured table
import sqlite3

try:
    database_connection = sqlite3.connect("blank_odm.sqlite")
    cursor = database_connection.cursor()
    print("Connection successful!")
except sqlite3.Error as e:
    print("Connection failed:", e)


# cursor.execute("PRAGMA table_info(methods);")
# columns = cursor.fetchall()
# print("The column name is below::")
# for col in columns:
#     print(col)


table_name = "site"

cursor.execute("""
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name=?;
""", (table_name,))
result = cursor.fetchone()

if result:
    print(f"Table '{table_name}' exists!")
else:
    print(f"Table '{table_name}' does NOT exist!")

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
        self.cursor.execute(query, values)

    def insert_many(self, table, data_list):
        for data in data_list:
            self.insert_row(table, data)

    def commit(self):
        self.conn.commit()

seeder = DatabaseSeeder(database_connection)

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

# source_data = [
#     {
#         "SourceID": 1,
#         "Organization": "USGS",
#         "City": "Logan",
#         "State": "UT"
#     }
# ]

seeder.insert_many("site", site_data)
seeder.commit()

