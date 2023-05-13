import unittest
from entities.transaction import Transaction


class TestTransaction(unittest.TestCase):
    # test id generation
    def test_generate_id(self):
        uid = Transaction.generate_id()

        self.assertEqual(len(uid), 36)

    # test getting date in correct format
    def test_get_due_date(self):
        trx = Transaction("test-id", "Test", 0, "2023-05-23 00:00:00")
        date = trx.get_due_date()

        self.assertEqual(date, "23.5.")

    # test getting amount in correct format
    def test_get_amount(self):
        trx = Transaction("test-id", "Test", 1500, "2023-05-23 00:00:00")
        amount = trx.get_amount()

        self.assertEqual(amount, 15.0)

    # test str method
    def test_str(self):
        uid = Transaction.generate_id()
        budget = Transaction(uid, "Test Transaction", 10000, "2023-05-09 16:00:00")

        self.assertEqual(str(budget), f"Test Transaction - 100.0€ - ID: {uid}")
