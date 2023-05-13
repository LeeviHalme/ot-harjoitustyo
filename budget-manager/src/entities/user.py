from uuid import uuid4


class User:
    """Describe the user object stored in the database without password

    Attributes:
        id: User's UUID
        name: User's name
        username: User's username
    """

    def __init__(self, user_id: str, name: str, username: str) -> None:
        self.id = user_id
        self.name = name
        self.username = username

    @staticmethod
    def generate_id() -> str:
        """Return a random UUID (version 4)

        Returns:
            str: Generated uuid
        """
        return str(uuid4())

    def __str__(self) -> str:
        return f"{self.name} (@{self.username}) - ID: {self.id}"
