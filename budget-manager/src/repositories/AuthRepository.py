from repositories.UserRepository import UserRepository, User
import bcrypt


class AuthRepository:
    def __init__(self, connection) -> None:
        self._user = None
        self._connection = connection
        self.user_repository = UserRepository(connection)

    # get user session
    def get_session(self):
        return self._user

    # validate hash and pass
    def _validate_password_hash(self, hashed: str, password: str) -> bool:
        # encoding user password
        bytes = password.encode("utf-8")
        hash_bytes = hashed.encode("utf-8")

        # checking password and return boolean
        return bcrypt.checkpw(bytes, hash_bytes)

    # hash given password
    def _generate_password_hash(self, password: str) -> str:
        # encoding user password
        bytes = password.encode("utf-8")

        # generating the salt
        salt = bcrypt.gensalt()

        pw_hash = bcrypt.hashpw(bytes, salt)

        # Hashing the password
        return pw_hash.decode("utf-8")

    # register a new user
    # returns boolean status flag
    def register_new_user(self, name: str, username: str, password: str) -> bool:
        # check if user exists
        user = self.user_repository.get_by_username(username)
        if user:
            return False

        # hash user password
        hash = self._generate_password_hash(password)

        self.user_repository.create_new_user(name, username, hash)

        # get user from db and store in state
        user = self.user_repository.get_by_username(username)
        self._user = User(user["id"], user["name"], user["username"])

        return True

    # login using username and password
    # returns boolean status flag
    def login_using_username_pass(self, username: str, password: str) -> bool:
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
