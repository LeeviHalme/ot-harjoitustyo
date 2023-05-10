from sqlite3 import Error as SQLError
from entities.Budget import Budget
from entities.Transaction import Transaction


class BudgetRepository:
    """Class used to manage user's budgets

    Attributes:
        _connection: Database connection
    """

    def __init__(self, connection) -> None:
        self._connection = connection

    def get_user_budgets(self, user_id: str) -> list:
        """Fetches all the budgets for a given user

        Args:
            user_id (str): User UID to fetch budgets for

        Returns:
            list: List of user's budgets
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "select id, name, description from budgets where user_id = :user_id",
            {"user_id": user_id},
        )

        rows = cursor.fetchall()

        return [
            Budget(row["id"], row["name"], row["description"], user_id) for row in rows
        ]

    def get_budget_by_id(self, budget_id: str) -> Budget:
        """Get a singular budget by id.
        Does not care about budget owner permissions.

        Args:
            budget_id (str): Budget UID to fetch

        Returns:
            Budget: Te fetched budget
        """
        try:
            cursor = self._connection.cursor()

            cursor.execute(
                "select id, name, description, user_id from budgets where id = :budget_id",
                {"budget_id": budget_id},
            )

            row = cursor.fetchone()

            return Budget(row["id"], row["name"], row["description"], row["user_id"])
        except SQLError as error:
            print(f"SQLError: {error}")
            return None

    def create_budget(self, name: str, description: str, user_id: str) -> Budget:
        """Create a new budget

        Args:
            name (str): Budget's name
            description (str): Budget's description
            user_id (str): User UID who created this budget

        Returns:
            Budget: The newly created budget
        """
        try:
            # generate new UUID for budget
            budget_id = Budget.generate_id()

            cursor = self._connection.cursor()

            cursor.execute(
                """insert into budgets (
                    id,
                    name,
                    description,
                    user_id
                )
                values (:id, :name, :description, :user_id)
                """,
                {
                    "id": budget_id,
                    "name": name,
                    "description": description,
                    "user_id": user_id,
                },
            )

            self._connection.commit()

            return Budget(budget_id, name, description, user_id)
        except SQLError as error:
            print(f"SQLError: {error}")
            return None

    def update_budget(self, budget_id: str, name: str, description: str) -> bool:
        """Perform update on existing budget

        Args:
            budget_id (str): Budget UID to update
            name (str): Input name
            description (str): Input description

        Returns:
            bool: Whether the update was successful
        """
        try:
            cursor = self._connection.cursor()

            cursor.execute(
                "update budgets set name = :name, description = :description WHERE id = :id",
                {"id": budget_id, "name": name, "description": description},
            )

            self._connection.commit()

            return True
        except SQLError as error:
            print(f"SQLError: {error}")
            return False

    def remove_budget_transactions(self, budget_id: str) -> bool:
        """Perform delete on existing budget transactions

        Args:
            budget_id (str): Budget UID to delete transactions from

        Returns:
            bool: Whether the deletion was successful
        """
        try:
            cursor = self._connection.cursor()

            cursor.execute(
                "delete from transactions WHERE budget_id = :id",
                {"id": budget_id},
            )

            self._connection.commit()

            return True
        except SQLError as error:
            print(f"SQLError: {error}")
            return False

    def remove_budget(self, budget_id: str) -> bool:
        """Perform delete on existing budget

        Args:
            budget_id (str): Budget UID to delete

        Returns:
            bool: Whether the deletion was successful
        """
        try:
            success = self.remove_budget_transactions(budget_id)
            if not success:
                return False

            cursor = self._connection.cursor()

            cursor.execute(
                "delete from budgets WHERE id = :id",
                {"id": budget_id},
            )

            self._connection.commit()

            return True
        except SQLError as error:
            print(f"SQLError: {error}")
            return False

    def get_current_month_transactions(self, budget_id: str) -> list:
        """Get all current month transactions for a single Budget and order by date

        Args:
            budget_id (str): Budget UID to fetch transactions for

        Returns:
            Transaction[]: List of all matched transactions
        """

        try:
            cursor = self._connection.cursor()

            cursor.execute(
                """
                select 
                  id,
                  name,
                  amount_cents,
                  due_at
                from
                  transactions
                where
                  budget_id = :budget_id
                and
                  strftime('%Y',due_at) = strftime('%Y',date('now'))
                and
                  strftime('%m',due_at) = strftime('%m',date('now'))
                order by
                  due_at DESC 
                """,
                {"budget_id": budget_id},
            )

            rows = cursor.fetchall()

            return [
                Transaction(row["id"], row["name"], row["amount_cents"], row["due_at"])
                for row in rows
            ]
        except SQLError as error:
            print(f"SQLError: {error}")
            return []

    def get_current_month_stats(self, budget_id: str) -> tuple:
        """Get current month statistics as a tuple

        Args:
            budget_id (str): _description_

        Returns:
            tuple: Tuple consisting of (balance: int, income: int, outcome: int)
        """
        transactions = self.get_current_month_transactions(budget_id)
        income = 0
        outcome = 0
        for trx in transactions:
            if trx.amount_cents > 0:
                income += trx.amount_cents
            else:
                outcome += trx.amount_cents
        balance = income + outcome

        return (balance / 100, income / 100, outcome / 100)

    def add_transaction(
        self, name: str, amount_cents: int, due_at: str, budget_id: str
    ) -> Transaction:
        """Create a new transaction

        Args:
            name (str): Describing name for the event
            amount_cents (int): Transaction amount in cents
            due_at (str): When this transaction is due
            budget_id (str): Corresponding Budget's UID

        Returns:
            Transaction: The newly created transaction
        """
        try:
            # generate new UUID for transaction
            transaction_id = Transaction.generate_id()

            cursor = self._connection.cursor()

            cursor.execute(
                """insert into transactions (
                    id,
                    name,
                    amount_cents,
                    due_at,
                    budget_id
                )
                values (:id, :name, :amount_cents, :due_at, :budget_id)
                """,
                {
                    "id": transaction_id,
                    "name": name,
                    "amount_cents": int(amount_cents),
                    "due_at": due_at,
                    "budget_id": budget_id,
                },
            )

            self._connection.commit()

            return Transaction(transaction_id, name, amount_cents, due_at)
        except SQLError as error:
            print(f"SQLError: {error}")
            return None

    def remove_transaction(self, transaction_id: str) -> bool:
        """Perform delete on existing transaction

        Args:
            transaction_id (str): Transaction UID to delete

        Returns:
            bool: Whether the deletion was successful
        """
        try:
            cursor = self._connection.cursor()

            cursor.execute(
                "delete from transactions WHERE id = :id",
                {"id": transaction_id},
            )

            self._connection.commit()

            return True
        except SQLError as error:
            print(f"SQLError: {error}")
            return False
