import os
import sqlite3

dirname = os.path.dirname(__file__)

# get db name from env
db_name = "test_database" if os.getenv("ENV_NAME") == "test" else "database"

path = os.path.join(dirname, "..", "..", "data", f"{db_name}.sqlite")

connection = sqlite3.connect(path)
connection.row_factory = sqlite3.Row


def get_database_connection():
    """Get current active database connection

    Returns:
        connection: SQLite connection object (refer to sqlite3 documentation)
    """
    return connection
