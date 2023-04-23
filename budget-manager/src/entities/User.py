from uuid import uuid4


class User:
    def __init__(self, id: str, name: str, username: str) -> None:
        self.id = id
        self.name = name
        self.username = username

    @staticmethod
    def generate_id():
        return str(uuid4())

    def __str__(self) -> str:
        return f"{self.name} (@{self.username}) - ID: {self.id}"
