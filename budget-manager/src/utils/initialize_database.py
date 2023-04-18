from connect_database import get_database_connection


# drop all existing tables
def drop_tables(connection):
    cursor = connection.cursor()

    # drop tables
    cursor.execute("drop table if exists users;")
    cursor.execute("drop table if exists budgets;")

    connection.commit()


# create tables
def create_tables(connection):
    cursor = connection.cursor()

    # create users table
    cursor.execute(
        """
        create table users (
            id TEXT NOT NULL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            username VARCHAR(100) NOT NULL,
            password_hash TEXT NOT NULL
        );
    """
    )

    # create budgets table
    cursor.execute(
        """
        create table budgets (
            id TEXT NOT NULL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            description VARCHAR(100) NOT NULL,
            user_id TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """
    )

    connection.commit()


# initialize db, drop and create
def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()