from views.LoginView import LoginView
from views.RegisterView import RegisterView


class UI:
    def __init__(self, window) -> None:
        self.window = window
        self.current_view = None

    def switch_view(self, view) -> None:
        self.current_view = view
        self.current_view.pack()

    # show budgets view
    def show_budgets(self) -> None:
        pass

    # show login view
    def show_login(self) -> None:
        view = LoginView(
            self.window,
            show_register=self.show_register,
            show_budgets=self.show_budgets,
        )
        self.switch_view(view)

    # show register view
    def show_register(self) -> None:
        view = RegisterView(self.window, show_login=self.show_login)
        self.switch_view(view)

    def start(self) -> None:
        # on init, show login screen
        self.show_login()
