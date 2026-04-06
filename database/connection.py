# A singleton design pattern is suggested to make sure all your file points to
# same database connection
import sqlite3


class DatabaseConnection:
    _instance = None

    def __init__(self):
        try:
            # Empty odm file should be at root directory of your project folder
            self.connection = sqlite3.connect("ndvi.sqlite")
            print("Connection successful!")
        except sqlite3.Error as e:
            print("Connection failed:", e)
            self.connection = None

    @classmethod
    def get_connection(cls):
        if cls._instance is None:
            cls._instance = DatabaseConnection()
        return cls._instance.connection


class DatabaseManager:
    def __init__(self):
        self.connection = DatabaseConnection.get_connection()
        self.cursor = self.connection.cursor()

    def insert_row(self, table, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        # for debugging whether the right query is inserted
        # print(query)
        self.cursor.execute(query, values)

    def insert_many(self, table, data_list):
        for data in data_list:
            self.insert_row(table, data)

    def commit_to_database(self):
        self.connection.commit()
