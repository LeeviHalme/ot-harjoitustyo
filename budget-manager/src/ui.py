from views.LoginView import LoginView


class UI:
    def __init__(self, window) -> None:
        self.window = window
        self.current_view = None

    def _login(self, username: str, password: str) -> bool:
        # log the user in
        print("do smth with data", username, password)

        return False

    def switch_view(self, view) -> None:
        self.current_view = view
        self.current_view.pack()

    def start(self) -> None:
        # on init, show login screen
        view = LoginView(self.window, self._login)
        self.switch_view(view)
