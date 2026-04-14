import sqlite3


class DatabaseConnection:
    def __init__(self, db_path="ndvi.sqlite"):
        try:
            self.connection = sqlite3.connect(db_path)
            self.connection.execute("PRAGMA journal_mode=WAL;")
            print("Connection successful!")
        except sqlite3.Error as e:
            print("Connection failed:", e)
            self.connection = None

    def get_connection(self):
        return self.connection


class DatabaseManager:
    def __init__(self):
        # give database path if your path is different
        connection = DatabaseConnection()
        self.connection = connection.get_connection()
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
