def drop_tables(connection):
    """Drop all existing data from database

    Args:
        connection: Database connection
    """
    cursor = connection.cursor()

    # drop tables
    cursor.execute("drop table if exists users;")
    cursor.execute("drop table if exists budgets;")
    cursor.execute("drop table if exists transactions;")

    connection.commit()


def create_tables(connection):
    """Create initial tables

    Args:
        connection: Database connection
    """
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

    # create transactions table
    cursor.execute(
        """
        create table transactions (
            id TEXT NOT NULL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            amount_cents INT NOT NULL,
            due_at TIMESTAMP NOT NULL,
            budget_id TEXT NOT NULL,
            FOREIGN KEY(budget_id) REFERENCES budgets(id)
        );
    """
    )

    connection.commit()


def initialize_database():
    """Initialize database by running the drop and create table-commands"""
    # pylint is disabled for below line because when running the file
    # with __name__ == "main" this is the correct way to import without
    # the tests breaking

    # pylint: disable=import-error,import-outside-toplevel
    from connect_database import get_database_connection

    # pylint: enable=import-error,import-outside-toplevel

    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":  # pragma: no cover
    initialize_database()
