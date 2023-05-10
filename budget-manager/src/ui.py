import sys
from views.LoginView import LoginView
from views.RegisterView import RegisterView
from views.BudgetsView import BudgetsView
from views.BudgetSummaryView import BudgetSummaryView


class UI:
    def __init__(self, window) -> None:
        self.window = window
        self.current_view = None
        self.user = None
        self.auto_login = False

        # check for cli args
        if len(sys.argv) > 1 and sys.argv[1] == "--autologin":
            self.auto_login = True

    def switch_view(self, view) -> None:
        if self.current_view:
            self.current_view.destroy()

        self.current_view = view
        self.current_view.pack()

    def add_session(self, user):
        self.user = user
        self.show_budgets()

    def delete_session(self):
        self.user = None
        self.show_login()

    def view_budget(self, budget_id: str) -> None:
        view = BudgetSummaryView(
            self.window,
            logout=self.delete_session,
            show_budgets=self.show_budgets,
            repack=lambda: self.view_budget(budget_id),
            user=self.user,
            budget_id=budget_id,
        )
        self.switch_view(view)

    def show_budgets(self) -> None:
        view = BudgetsView(
            self.window,
            view_budget=self.view_budget,
            logout=self.delete_session,
            repack=self.show_budgets,
            user=self.user,
        )
        self.switch_view(view)

    def show_login(self) -> None:
        view = LoginView(
            self.window,
            show_register=self.show_register,
            add_session=self.add_session,
        )
        self.switch_view(view)

    def show_register(self) -> None:
        view = RegisterView(self.window, show_login=self.show_login)
        self.switch_view(view)

    # automatically login with test account
    # only to be used in development
    def __auto_login(self):
        from utils.connect_database import get_database_connection
        from repositories.AuthRepository import AuthRepository

        connection = get_database_connection()
        repository = AuthRepository(connection)
        success = repository.login_using_username_pass("leehalme", "testi")
        if not success:
            return print("AUTO-LOGIN FAILED")
        user = repository.get_session()
        self.add_session(user)

    def start(self) -> None:
        # on init, show login screen
        self.show_login()

        # Only in development
        if self.auto_login:
            self.__auto_login()
