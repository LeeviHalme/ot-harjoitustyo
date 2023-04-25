from views.LoginView import LoginView
from views.RegisterView import RegisterView
from views.BudgetsView import BudgetsView


class UI:
    def __init__(self, window) -> None:
        self.window = window
        self.current_view = None
        self.user = None

    def switch_view(self, view) -> None:
        if self.current_view:
            self.current_view.destroy()

        self.current_view = view
        self.current_view.pack()

    # add session
    def add_session(self, user):
        self.user = user
        self.show_budgets()

    # delete session
    def delete_session(self):
        self.user = None
        self.show_login()

    # show singular budget page
    def view_budget(self) -> None:
        pass

    # show budgets view
    def show_budgets(self) -> None:
        view = BudgetsView(
            self.window,
            view_budget=self.view_budget,
            logout=self.delete_session,
            repack=self.show_budgets,
            user=self.user,
        )
        self.switch_view(view)

    # show login view
    def show_login(self) -> None:
        view = LoginView(
            self.window,
            show_register=self.show_register,
            add_session=self.add_session,
        )
        self.switch_view(view)

    # show register view
    def show_register(self) -> None:
        view = RegisterView(self.window, show_login=self.show_login)
        self.switch_view(view)

    def start(self) -> None:
        # on init, show login screen
        self.show_login()
