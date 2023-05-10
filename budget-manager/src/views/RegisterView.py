import tkinter
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from utils.connect_database import get_database_connection
from repositories.AuthRepository import AuthRepository


class RegisterView:
    """Class used to show login view

    Attributes:
        window (Ctk):                       CustomTkInter Main Window
        frame (CtkFrame | None):            Root frame for this view

        login_view (function):              Show LoginView

        repository (AuthRepository):        Authentication repository instance

        title (str):                        Title shown on the page
        subtitle (str):                     Subtitle shown on the page
        name_entry (CtkEntry):              State variable for name input
        username_entry (CtkEntry):          State variable for username input
        password_entry (CtkEntry):          State variable for password input
        password_confirm_entry (CtkEntry):  State variable for password confirmation input
    """

    def __init__(self, window, show_login) -> None:
        self.window = window
        self.frame = None
        self.login_view = show_login

        # declare repositories
        connection = get_database_connection()
        self.repository = AuthRepository(connection)

        # declare text variables
        self.title = "Budjetointisovellus"
        self.subtitle = "Hallitse talouttasi tehokkaasti budjetointisovelluksen avulla. Voit lisätä henkilökohtaiseen budjettiisi koko kuukauden menot, tulot ja yllättävät kulut. Voit myös hallita useita budjetteja samalla käyttäjällä."

        # declare state
        self.name_entry = None
        self.username_entry = None
        self.password_entry = None
        self.password_confirm_entry = None

        self.init()

    def register(self):
        """Button click handler for registering a new user"""
        if (
            not self.name_entry
            or not self.username_entry
            or not self.password_entry
            or not self.password_confirm_entry
        ):
            return

        # get vars from state
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_confirm = self.password_confirm_entry.get()

        # if passwords won't match
        if password != password_confirm:
            tkinter.messagebox.showerror(
                title="Rekisteröinti epäonnistui", message="Salasanat eivät täsmää!"
            )
            return

        # loose validation that values exist
        if not name or not username or not password:
            tkinter.messagebox.showinfo(
                title="Hups!",
                message="Nimi, käyttäjänimi tai salasana eivät saa olla tyhjiä",
            )
            return

        # if register wasn't successful
        success = self.repository.register_new_user(name, username, password)
        if not success:
            tkinter.messagebox.showerror(
                title="Rekisteröinti epäonnistui",
                message="Tällä käyttätunnuksella on jo tili!",
            )
            return

        # redirect to login view
        tkinter.messagebox.showinfo(
            title="Rekisteröinti onnistui!",
            message="Käyttäjätili luotu. Voit nyt kirjautua sisään.",
        )
        self.login_view()

    def pack(self):
        """Pack (use grid) the current frame into the window"""
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def destroy(self):
        """Destroy current frame"""
        self.frame.destroy()

    def init(self):
        """Main method to draw and initiate the view"""
        self.frame = CTkFrame(self.window, fg_color="transparent")

        # configure layout
        self.frame.columnconfigure(0, weight=2)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=2)

        # create frame for text elements
        f1 = CTkFrame(self.frame)
        f1.columnconfigure(0, weight=1)
        f1.rowconfigure(0, weight=1)
        f1.rowconfigure(1, weight=2)
        f1.grid(row=0, column=0, sticky="nswe")

        # create text elements
        l1 = CTkLabel(f1, text=self.title, font=("Monospace", 32, "bold"))
        l2 = CTkLabel(
            f1,
            text=self.subtitle,
            wraplength=450,
            font=("Monospace", 18),
            justify="left",
        )
        l1.grid(row=0, column=0, sticky="w", padx=(20, 0))
        l2.grid(row=1, column=0, sticky="wn", padx=(20, 0))

        # create frame for inputs
        f2 = CTkFrame(self.frame)
        f2.columnconfigure(0, weight=1)
        f2.columnconfigure(1, weight=2)
        f2.rowconfigure(0, weight=1)
        f2.rowconfigure(1, weight=1)
        f2.rowconfigure(2, weight=1)
        f2.rowconfigure(3, weight=1)
        f2.rowconfigure(4, weight=1)
        f2.grid(row=0, column=1, sticky="nswe", padx=(15, 0))

        # create inputs and their labels
        l3 = CTkLabel(f2, text="Nimi")
        l4 = CTkLabel(f2, text="Käyttäjätunnus")
        l5 = CTkLabel(f2, text="Salasana")
        l6 = CTkLabel(f2, text="Salasana uudelleen")
        self.name_entry = CTkEntry(f2, placeholder_text="Matti Meikäläinen")
        self.username_entry = CTkEntry(f2, placeholder_text="mattimeika")
        self.password_entry = CTkEntry(f2, placeholder_text="**************", show="*")
        self.password_confirm_entry = CTkEntry(
            f2, placeholder_text="**************", show="*"
        )
        l3.grid(row=0, column=0, sticky="w", padx=(20, 0))
        l4.grid(row=1, column=0, sticky="w", padx=(20, 0))
        l5.grid(row=2, column=0, sticky="w", padx=(20, 0))
        l6.grid(row=3, column=0, sticky="w", padx=(20, 0))
        self.name_entry.grid(row=0, column=1, sticky="we", padx=(0, 20))
        self.username_entry.grid(row=1, column=1, sticky="we", padx=(0, 20))
        self.password_entry.grid(row=2, column=1, sticky="we", padx=(0, 20))
        self.password_confirm_entry.grid(row=3, column=1, sticky="we", padx=(0, 20))

        # create buttons
        b1 = CTkButton(f2, text="Rekisteröidy", command=self.register)
        b2 = CTkButton(f2, text="← Takaisin", command=self.login_view, fg_color="gray")
        b1.grid(row=4, column=0, sticky="we", padx=15)
        b2.grid(row=4, column=1, sticky="we", padx=15)
