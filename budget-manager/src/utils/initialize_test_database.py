from utils.connect_database import get_database_connection
from utils.initialize_database import drop_tables, create_tables
from repositories.UserRepository import User
from repositories.AuthRepository import AuthRepository


# initialize db, drop and create
def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


# insert testing data
def insert_test_data():
    connection = get_database_connection()
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
