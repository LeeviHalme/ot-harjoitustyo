from datetime import datetime
from uuid import uuid4


class Transaction:
    """Describe the transaction object stored in the database

    Attributes:
        id: Transactions's UUID
        name: Description of the event
        amount_cents: Transaction amount in cents (can be negative)
        due_at: SQLite timestamp of the due date
    """

    def __init__(
        self, transaction_id: str, name: str, amount_cents: int, due_at: str
    ) -> None:
        self.id = transaction_id
        self.name = name
        self.amount_cents = amount_cents
        self.due_at = due_at

    @staticmethod
    def generate_id() -> str:
        """Return a random UUID (version 4)

        Returns:
            str: Generated uuid
        """
        return str(uuid4())

    def _format_cents(self, amount: int) -> float:
        return amount / 100

    def _format_date(self, date: str) -> str:
        parsed = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        return f"{parsed.day}.{parsed.month}."

    def get_amount(self) -> float:
        """Get transaction amount in euros

        Returns:
            float: Amount in euros
        """
        return self._format_cents(self.amount_cents)

    def get_due_date(self) -> str:
        """Get transaction due date as datetime

        Returns:
            datetime: Due date
        """
        return self._format_date(self.due_at)

    def __str__(self) -> str:
        return f"{self.name}- {self._format_cents(self.amount_cents)}€ - ID: {self.id}"
