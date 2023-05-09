import unittest
from entities.Transaction import Transaction


class TestTransaction(unittest.TestCase):
    # test id generation
    def test_generate_id(self):
        uid = Transaction.generate_id()

        self.assertEqual(len(uid), 36)

    # test str method
    def test_str(self):
        uid = Transaction.generate_id()
        budget = Transaction(uid, "Test Transaction", 10000, "2023-05-09 16:00:00")

        self.assertEqual(str(budget), f"Test Transaction - 100.0€ - ID: {uid}")
