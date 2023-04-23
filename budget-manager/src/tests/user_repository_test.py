import unittest
from utils.connect_database import get_database_connection
from utils.initialize_database import initialize_database, insert_test_data
from repositories.UserRepository import UserRepository, User


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


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        # setup db connection
        initialize_database()
        self._connection = get_database_connection()
        insert_test_data(self._connection)

    # test get user by username
    def test_get_by_username(self):
        repository = UserRepository(self._connection)
        result = repository.get_by_username("test")

        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "TestAccount")
        self.assertEqual(result["username"], "test")
        self.assertEqual(len(result["password_hash"]), 60)
