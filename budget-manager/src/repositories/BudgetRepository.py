from sqlite3 import Error as SQLError
from entities.Budget import Budget


class BudgetRepository:
    """Class used to manage user's budgets

    Attributes:
        _connection: Database connection
    """

    def __init__(self, connection) -> None:
        self._connection = connection

    # get user budgets
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

    # get budget by id
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
            print(error)
            return None

    # create a new budget
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
            print(error)
            return None

    # update budget name and description
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
            print(error)
            return False
