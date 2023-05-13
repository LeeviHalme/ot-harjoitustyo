import unittest
from entities.user import User


class TestUser(unittest.TestCase):
    # test id generation
    def test_generate_id(self):
        uid = User.generate_id()

        self.assertEqual(len(uid), 36)

    # test user str method
    def test_str(self):
        uid = User.generate_id()
        user = User(uid, "TestAccount", "test")

        self.assertEqual(str(user), f"TestAccount (@test) - ID: {uid}")
