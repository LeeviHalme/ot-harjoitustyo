import os
import sqlite3

dirname = os.path.dirname(__file__)
path = os.path.join(dirname, "..", "..", "data", "database.sqlite")

connection = sqlite3.connect(path)
connection.row_factory = sqlite3.Row


def get_database_connection():
    return connection
