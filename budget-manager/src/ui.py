from views.LoginView import LoginView


class UI:
    def __init__(self, window) -> None:
        self.window = window
        self.current_view = None

    def switch_view(self, view) -> None:
        self.current_view = view
        self.current_view.pack()

    def start(self) -> None:
        # on init, show login screen
        view = LoginView(self.window)
        self.switch_view(view)
