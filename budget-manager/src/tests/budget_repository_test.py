import unittest
from utils.connect_database import get_database_connection
from utils.initialize_test_database import initialize_database, insert_test_data
from repositories.BudgetRepository import BudgetRepository


class TestBudgetRepository(unittest.TestCase):
    def setUp(self):
        # setup db connection
        initialize_database()
        self._connection = get_database_connection()

        # insert test data
        user_id, budget_id, trx_ids = insert_test_data()
        self.user_id = user_id
        self.budget_id = budget_id
        self.trx_ids = trx_ids

    def test_get_user_budgets(self):
        repository = BudgetRepository(self._connection)
        budgets = repository.get_user_budgets(self.user_id)

        self.assertEqual(len(budgets), 1)
        self.assertEqual(budgets[0].name, "Test Budget")
        self.assertEqual(budgets[0].description, "Example Description")

    def test_get_budget_by_id(self):
        repository = BudgetRepository(self._connection)
        budget = repository.get_budget_by_id(self.budget_id)

        self.assertIsNotNone(budget)
        self.assertEqual(budget.name, "Test Budget")
        self.assertEqual(budget.description, "Example Description")

    def test_create_budget(self):
        repository = BudgetRepository(self._connection)
        name, description = ("Test Budget 2", "Example Description")

        created_budget = repository.create_budget(name, description, self.user_id)

        self.assertIsNotNone(created_budget)
        self.assertEqual(created_budget.name, "Test Budget 2")
        self.assertEqual(created_budget.description, "Example Description")

    def test_update_budget(self):
        repository = BudgetRepository(self._connection)
        name, description = ("Test Renamed Budget 2", "Example Renamed Description")

        success = repository.update_budget(self.budget_id, name, description)
        budget = repository.get_budget_by_id(self.budget_id)

        self.assertTrue(success)
        self.assertIsNotNone(budget)
        self.assertEqual(budget.name, "Test Renamed Budget 2")
        self.assertEqual(budget.description, "Example Renamed Description")

    def test_remove_budget(self):
        repository = BudgetRepository(self._connection)

        success = repository.remove_budget(self.budget_id)
        budget = repository.get_budget_by_id(self.budget_id)

        self.assertTrue(success)
        self.assertIsNone(budget)

    def test_get_current_month_transactions(self):
        repository = BudgetRepository(self._connection)

        transactions = repository.get_current_month_transactions(self.budget_id)

        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].name, "Test Transaction 2")
        self.assertEqual(transactions[0].amount_cents, -7500)

        # assert correct format dd.mm.
        date = transactions[0].get_due_date()
        self.assertEqual(date.split(".")[0], "2")

    def test_get_current_month_stats(self):
        repository = BudgetRepository(self._connection)

        balance, income, outcome = repository.get_current_month_stats(self.budget_id)

        self.assertIsNotNone(balance)
        self.assertIsNotNone(income)
        self.assertIsNotNone(outcome)

        self.assertEqual(balance, 75.0)
        self.assertEqual(income, 150.0)
        self.assertEqual(outcome, -75.0)

    def test_add_transaction(self):
        repository = BudgetRepository(self._connection)
        name, amount_cents, due_at = ("Test Trx", 1250, "2023-05-13 00:00:00")

        trx = repository.add_transaction(name, amount_cents, due_at, self.budget_id)

        self.assertIsNotNone(trx)
        self.assertEqual(trx.name, "Test Trx")
        self.assertEqual(trx.amount_cents, 1250)
        self.assertEqual(trx.due_at, "2023-05-13 00:00:00")

    def test_remove_transaction(self):
        repository = BudgetRepository(self._connection)

        success = repository.remove_transaction(self.trx_ids[0])
        transactions = repository.get_current_month_transactions(self.budget_id)

        self.assertTrue(success)
        self.assertEqual(len(transactions), 1)
