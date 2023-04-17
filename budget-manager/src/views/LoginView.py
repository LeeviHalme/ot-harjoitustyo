from tkinter import ttk, constants


class LoginView:
    def __init__(self, window) -> None:
        self.window = window
        self.frame = None

        self.init()

    def pack(self):
        self.frame.pack(fill=constants.X)

    def destroy(self):
        self.frame.destroy()

    def init(self):
        self.frame = ttk.Frame(self.window, padding=25)

        # title
        ttk.Label(
            self.frame,
            text="Budjetointisovellus",
            anchor="w",
            font="Times 32",
        ).grid(row=0, column=0)

        # subtitle
        ttk.Label(
            self.frame,
            anchor="w",
            font="16",
            text="Hallitse talouttasi tehokkaasti budjetointisovelluksen\navulla. Voit lisätä henkilökohtaiseen budjettiisi koko\nkuukauden menot, tulot ja yllättävät kulut. Voit myös\nhallita useita budjetteja samalla käyttäjällä.",
        ).grid(row=1, column=0, pady=10, rowspan=3)

        # username label and entry
        ttk.Label(self.frame, text="Käyttäjätunnus").grid(row=0, column=1)
        ttk.Entry(self.frame).grid(row=0, column=2, padx=10, columnspan=2)

        # password label and entry
        ttk.Label(self.frame, text="Salasana").grid(row=1, column=1)
        ttk.Entry(self.frame).grid(row=1, column=2, padx=10, columnspan=2)

        # login and register buttons
        ttk.Button(self.frame, text="Kirjaudu").grid(row=2, column=2)
        ttk.Button(self.frame, text="Rekisteröidy").grid(row=2, column=3)
