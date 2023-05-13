from datetime import date
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


def insert_test_data() -> tuple:
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
    budget = budget_repository.create_budget(
        "Test Budget", "Example Description", user.id
    )

    # insert transactions
    year = date.today().year
    month_num = date.today().month
    other_month_num = month_num + 1 if month_num < 12 else month_num - 1
    month = month_num if int(month_num) > 10 else f"0{month_num}"
    other_month = (
        other_month_num if int(other_month_num) > 10 else f"0{other_month_num}"
    )
    trx_1 = budget_repository.add_transaction(
        "Test Transaction", 15000, f"{year}-{month}-01 00:00:00", budget.id
    )
    trx_2 = budget_repository.add_transaction(
        "Test Transaction 2", -7500, f"{year}-{month}-02 00:00:00", budget.id
    )
    trx_3 = budget_repository.add_transaction(
        "Test Transaction 3", 15000, f"{year}-{other_month}-01 00:00:00", budget.id
    )

    return (user.id, budget.id, [trx_1.id, trx_2.id, trx_3.id])
