from repositories.UserRepository import UserRepository
import bcrypt


class User:
    def __init__(self, id: str, name: str, username: str) -> None:
        self.id = id
        self.name = name
        self.username = username


class AuthRepository:
    def __init__(self, connection) -> None:
        self._connection = connection
        self.user_repository = UserRepository(connection)
        self.user = None

    # get user session
    def get_session(self):
        return self.user

    # validate hash and pass
    def _validatePasswordHash(hashed: str, password: str):
        # encoding user password
        bytes = password.encode("utf-8")

        # checking password and return boolean
        return bcrypt.checkpw(bytes, hashed)

    # returns boolean status flag
    def loginUsingUsernamePass(self, username: str, password: str) -> bool:
        # check if user doesn't exists
        user = self.user_repository.get_by_username(username)
        if not user:
            return False

        # validate password hash
        valid = self._validatePasswordHash(user["password_hash"], password)
        if not valid:
            return False

        # keep user session at state
        self.user = User(user["id"], user["name"], user["username"])

        return True
