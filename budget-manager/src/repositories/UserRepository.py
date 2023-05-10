from sqlite3 import Error as SQLError
from entities.User import User


class UserRepository:
    """Class used to query user information

    Attributes:
        _connection: Database connection
    """

    def __init__(self, connection) -> None:
        self._connection = connection

    # get user by username
    def get_by_username(self, username: str):
        """Get user object by their username

        Args:
            username (str): Input username

        Returns:
            User: Dictionary of a raw user object. (fixme: should probably return User)
        """
        try:
            cursor = self._connection.cursor()

            cursor.execute(
                "select id, name, username, password_hash from users where username = :username",
                {"username": username},
            )

            row = cursor.fetchone()

            if not row:
                return None

            return dict(row)
        except SQLError as error:
            print(error)
            return None

    # create new user
    def create_new_user(self, name: str, username: str, password_hash: str) -> bool:
        """Creates a new user on the db

        Args:
            name (str): Input user's name
            username (str): Input user's username
            password_hash (str): Input user's hashed password
        """
        # generate new UUID for user
        user_id = User.generate_id()

        try:
            cursor = self._connection.cursor()

            cursor.execute(
                "insert into users (id, name, username, password_hash) values (:id, :name, :username, :hash)",
                {
                    "id": user_id,
                    "name": name,
                    "username": username,
                    "hash": password_hash,
                },
            )

            self._connection.commit()

            return True
        except SQLError as error:
            print(error)
            return False
