import unittest
from entities.Budget import Budget


class TestBudget(unittest.TestCase):
    # test id generation
    def test_generate_id(self):
        uid = Budget.generate_id()

        self.assertEqual(len(uid), 36)

    # test str method
    def test_str(self):
        uid = Budget.generate_id()
        budget = Budget(uid, "TestBudget", "test_description", "ExampleID")

        self.assertEqual(
            str(budget), f"TestBudget / test_description - ID: {uid} - Owner: ExampleID"
        )
