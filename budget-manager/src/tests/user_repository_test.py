import unittest
from utils.connect_database import get_database_connection
from utils.initialize_test_database import initialize_database, insert_test_data
from repositories.UserRepository import UserRepository


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        # setup db connection
        initialize_database()
        self._connection = get_database_connection()
        insert_test_data()

    # test get user by username
    def test_get_by_username(self):
        repository = UserRepository(self._connection)
        result = repository.get_by_username("test")

        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "TestAccount")
        self.assertEqual(result["username"], "test")
        self.assertEqual(len(result["password_hash"]), 60)
