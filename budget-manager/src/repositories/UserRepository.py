from uuid import uuid4


class User:
    def __init__(self, id: str, name: str, username: str) -> None:
        self.id = id
        self.name = name
        self.username = username

    def generate_id():
        return str(uuid4())

    def __str__(self) -> str:
        return f"{self.name} (@{self.username}) - ID: {self.id}"


class UserRepository:
    def __init__(self, connection) -> None:
        self._connection = connection

    # get user by username
    def get_by_username(self, username: str):
        cursor = self._connection.cursor()

        cursor.execute(
            "select id, name, username, password_hash from users where username = :username",
            {"username": username},
        )

        row = cursor.fetchone()

        if not row:
            return None

        return dict(row)

    # create new user
    def create_new_user(self, name: str, username: str, password_hash: str) -> None:
        # generate new UUID for user
        user_id = User.generate_id()

        cursor = self._connection.cursor()

        cursor.execute(
            "insert into users (id, name, username, password_hash) values (:id, :name, :username, :hash)",
            {"id": user_id, "name": name, "username": username, "hash": password_hash},
        )

        self._connection.commit()

        return
