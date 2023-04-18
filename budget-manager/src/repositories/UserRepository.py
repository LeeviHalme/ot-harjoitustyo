class UserRepository:
    def __init__(self, connection) -> None:
        self._connection = connection

    # get user by username
    def get_by_username(self, username: str):
        cursor = self._connection.cursor()

        cursor.execute(
            "select username, password_hash from users where username = :username",
            {"username": username},
        )

        row = cursor.fetchone()

        if not row:
            return None

        return dict(row)
