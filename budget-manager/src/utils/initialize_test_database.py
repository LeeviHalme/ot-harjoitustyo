from utils.connect_database import get_database_connection
from utils.initialize_database import drop_tables, create_tables
from repositories.AuthRepository import AuthRepository
from repositories.BudgetRepository import BudgetRepository


def initialize_database():
    """Initialize database by dropping existing tables
    (data) and creating new empty tables
    """
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


def insert_test_data():
    """Inserts data to the db in order to perform tests
    on the repository methods
    """
    connection = get_database_connection()
    auth_repository = AuthRepository(connection)
    budget_repository = BudgetRepository(connection)

    # insert user
    auth_repository.register_new_user("Testaaja Teppo", "test", "test")
    user = auth_repository.get_session()

    # insert budget
    budget_repository.create_budget("Test Budget", "Example description", user.id)
