from uuid import uuid4


class Budget:
    def __init__(self, id: str, name: str, description: str, user_id: str) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.user_id = user_id

    @staticmethod
    def generate_id():
        return str(uuid4())

    def __str__(self) -> str:
        return (
            f"{self.name} / {self.description} - ID: {self.id} - Owner: {self.user_id}"
        )
