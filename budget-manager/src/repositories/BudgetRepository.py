from sqlite3 import Error as SQLError
from entities.Budget import Budget


class BudgetRepository:
    def __init__(self, connection) -> None:
        self._connection = connection

    # get user budgets
    def get_user_budgets(self, user_id: str) -> list[Budget] or None:
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
    def get_budget_by_id(self, budget_id: str) -> Budget | None:
        try:
            cursor = self._connection.cursor()

            cursor.execute(
                "select id, name, description, user_id from budgets where budget_id = :budget_id",
                {"budget_id": budget_id},
            )

            row = cursor.fetchone()

            return Budget(row["id"], row["name"], row["description"], row["user_id"])
        except SQLError as error:
            print(error)
            return None

    # create a new budget
    def create_budget(self, name: str, description: str, user_id: str) -> Budget | None:
        try:
            # generate new UUID for budget
            budget_id = Budget.generate_id()

            cursor = self._connection.cursor()

            cursor.execute(
                "insert into budgets (id, name, description, user_id) values (:id, :name, :description, :user_id)",
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
