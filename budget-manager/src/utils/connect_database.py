import os
import sqlite3

dirname = os.path.dirname(__file__)
path = os.path.join(dirname, "..", "..", "data", "database.sqlite")

connection = sqlite3.connect(path)
connection.row_factory = sqlite3.Row


def get_database_connection():
    """Get current active database connection

    Returns:
        connection: SQLite connection object (refer to sqlite3 documentation)
    """
    return connection
