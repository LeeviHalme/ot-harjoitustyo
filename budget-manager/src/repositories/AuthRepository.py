import bcrypt
from repositories.UserRepository import UserRepository
from entities.User import User


class AuthRepository:
    """Class used to authenticate users

    Attributes:
        _user: User in session
        _connection: Database connection
        user_repository: Reference to a UserRepository instance
    """

    def __init__(self, connection) -> None:
        self._user = None
        self._connection = connection
        self.user_repository = UserRepository(connection)

    def get_session(self) -> User:
        """Returns the current user in session

        Returns:
            User | None: User in session, or None if no session
        """
        return self._user

    def _validate_password_hash(self, hashed: str, password: str) -> bool:
        # encoding user password
        pwd_bytes = password.encode("utf-8")
        hash_bytes = hashed.encode("utf-8")

        # checking password and return boolean
        return bcrypt.checkpw(pwd_bytes, hash_bytes)

    def _generate_password_hash(self, password: str) -> str:
        # encoding user password
        pwd_bytes = password.encode("utf-8")

        # generating the salt
        salt = bcrypt.gensalt()

        # Hashing the password
        pw_hash = bcrypt.hashpw(pwd_bytes, salt)

        return pw_hash.decode("utf-8")

    def register_new_user(self, name: str, username: str, password: str) -> bool:
        """Registers a new user

        Args:
            name (str): User's name
            username (str): User's username
            password (str): User's plaintext password

        Returns:
            bool: Whether the creation was successful
        """
        # check if user exists
        user = self.user_repository.get_by_username(username)
        if user:
            return False

        # hash user password
        hashed = self._generate_password_hash(password)

        success = self.user_repository.create_new_user(name, username, hashed)
        if not success:
            return False

        # store in state
        user = self.user_repository.get_by_username(username)
        self._user = User(user["id"], user["name"], user["username"])

        return True

    def login_using_username_pass(self, username: str, password: str) -> bool:
        """Login to an existing account with username and password

        Args:
            username (str): Input username
            password (str): Input password

        Returns:
            bool: Whether login was successful
        """
        # check if user doesn't exist
        user = self.user_repository.get_by_username(username)
        if not user:
            return False

        # validate password hash
        valid = self._validate_password_hash(user["password_hash"], password)
        if not valid:
            return False

        # keep user session at state
        self._user = User(user["id"], user["name"], user["username"])

        return True
