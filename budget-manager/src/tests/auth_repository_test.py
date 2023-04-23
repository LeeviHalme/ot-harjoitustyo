import unittest
from utils.connect_database import get_database_connection
from utils.initialize_database import initialize_database, insert_test_data
from repositories.AuthRepository import AuthRepository


class TestAuthRepository(unittest.TestCase):
    def setUp(self):
        # setup db connection
        initialize_database()
        self._connection = get_database_connection()

    # tests session getter on init
    def test_get_session_init(self):
        repository = AuthRepository(self._connection)
        session = repository.get_session()
        self.assertEqual(session, None)

    # test hash validation
    def test_validate_password_hash(self):
        repository = AuthRepository(self._connection)
        hash = repository._generate_password_hash("test")
        valid = repository._validate_password_hash(hash, "test")
        self.assertTrue(valid)

    # test registering a new user
    def test_register_new_user(self):
        repository = AuthRepository(self._connection)
        name, username, password = ("test", "test", "test")

        success = repository.register_new_user(name, username, password)
        user = repository._user

        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "test")
        self.assertEqual(user.username, "test")

    # test logging in
    def test_login_using_username_pass(self):
        repository_1 = AuthRepository(self._connection)
        repository_2 = AuthRepository(self._connection)
        name, username, password = ("test", "test", "test")
        repository_1.register_new_user(name, username, password)

        # use repository_2 to get fresh session
        success = repository_2.login_using_username_pass(username, password)
        user = repository_2._user

        self.assertTrue(success)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "test")
        self.assertEqual(user.username, "test")

    # test registering an existing user
    def test_register_existing_user(self):
        # insert test data
        insert_test_data(self._connection)

        repository = AuthRepository(self._connection)
        name, username, password = ("test", "test", "test")

        success = repository.register_new_user(name, username, password)

        self.assertFalse(success)
        self.assertIsNone(repository._user)

    # test logging in with invalid username
    def test_login_invalid_username(self):
        repository = AuthRepository(self._connection)
        username, password = ("test", "test")

        success = repository.login_using_username_pass(username, password)

        self.assertFalse(success)
        self.assertIsNone(repository._user)

    # test logging in with invalid password
    def test_login_invalid_password(self):
        # insert test data
        insert_test_data(self._connection)

        repository = AuthRepository(self._connection)
        username, password = ("test", "invalid")

        success = repository.login_using_username_pass(username, password)

        self.assertFalse(success)
        self.assertIsNone(repository._user)
