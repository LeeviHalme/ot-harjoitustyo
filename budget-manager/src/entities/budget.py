from uuid import uuid4


class Budget:
    """Describe the Budget object stored in the database

    Attributes:
        id: Budget's UUID
        name: Budget's name
        description: Budget's description
        user_id: UUID of User who created this Budget
    """

    def __init__(
        self, budget_id: str, name: str, description: str, user_id: str
    ) -> None:
        self.id = budget_id
        self.name = name
        self.description = description
        self.user_id = user_id

    @staticmethod
    def generate_id():
        """Return a random UUID (version 4)

        Returns:
            str: Generated uuid
        """
        return str(uuid4())

    def __str__(self) -> str:
        return (
            f"{self.name} / {self.description} - ID: {self.id} - Owner: {self.user_id}"
        )
