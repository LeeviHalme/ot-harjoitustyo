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


# insert testing data
def insert_test_data(connection):
    from repositories.UserRepository import User
    from repositories.AuthRepository import AuthRepository

    cursor = connection.cursor()

    # insert user
    user_id = User.generate_id()
    repo = AuthRepository(connection)
    hash = repo._generate_password_hash(password="test")
    cursor.execute(
        """
        insert into users (id, name, username, password_hash)
        values (:id, 'TestAccount', 'test', :hash)
        """,
        {"id": user_id, "hash": hash},
    )

    # insert budget
    budget_id = User.generate_id()
    cursor.execute(
        """
        insert into budgets (id, name, description, user_id)
        values (:id, 'TestBudget', 'Test', :user_id)
        """,
        {"id": budget_id, "user_id": user_id},
    )

    connection.commit()


# initialize db, drop and create
def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":  # pragma: no cover
    initialize_database()
