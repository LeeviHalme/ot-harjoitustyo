import tkinter
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from utils.connect_database import get_database_connection
from repositories.AuthRepository import AuthRepository


class LoginView:
    """Class used to show login view

    Attributes:
        window (Ctk):                   CustomTkInter Main Window
        frame (CtkFrame | None):        Root frame for this view

        register_view (function):       Show RegisterView
        add_session (function):         Add user session to UI state

        repository (AuthRepository):    Authentication repository instance

        title (str):                    Title shown on the page
        subtitle (str):                 Subtitle shown on the page
        username_entry (CtkEntry):      State variable for username input
        password_entry (CtkEntry):      State variable for password input
    """

    def __init__(self, window, show_register, add_session) -> None:
        self.window = window
        self.frame = None
        self.register_view = show_register
        self.add_session = add_session

        # declare repositories
        connection = get_database_connection()
        self.repository = AuthRepository(connection)

        # declare text variables
        self.title = "Budjetointisovellus"
        self.subtitle = "Hallitse talouttasi tehokkaasti budjetointisovelluksen avulla. Voit lisätä henkilökohtaiseen budjettiisi koko kuukauden menot, tulot ja yllättävät kulut. Voit myös hallita useita budjetteja samalla käyttäjällä."

        # declare state
        self.username_entry = None
        self.password_entry = None

        self.init()

    # login user using local auth
    def login(self):
        """Button click handler for logging in"""
        if not self.username_entry or not self.password_entry:
            return

        # get vars from state
        username = self.username_entry.get()
        password = self.password_entry.get()

        # use repository method
        success = self.repository.login_using_username_pass(username, password)

        # if login wasn't successful
        if not success:
            tkinter.messagebox.showerror(
                title="Hups!", message="Väärä käyttäjätunnus tai salasana."
            )
            return

        # add session and redirect to budgets view
        session = self.repository.get_session()
        self.add_session(session)

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
        f2.grid(row=0, column=1, sticky="nswe", padx=(15, 0))

        # create inputs and their labels
        l3 = CTkLabel(f2, text="Käyttäjätunnus")
        l4 = CTkLabel(f2, text="Salasana")
        self.username_entry = CTkEntry(f2, placeholder_text="mattimeika")
        self.password_entry = CTkEntry(f2, placeholder_text="**************", show="*")
        l3.grid(row=0, column=0, sticky="w", padx=(20, 0))
        l4.grid(row=1, column=0, sticky="w", padx=(20, 0))
        self.username_entry.grid(row=0, column=1, sticky="we", padx=(0, 20))
        self.password_entry.grid(row=1, column=1, sticky="we", padx=(0, 20))

        # create buttons
        b1 = CTkButton(f2, text="Kirjaudu", command=self.login)
        b2 = CTkButton(
            f2, text="Rekisteröidy", command=self.register_view, fg_color="gray"
        )
        b1.grid(row=2, column=0, sticky="we", padx=15)
        b2.grid(row=2, column=1, sticky="we", padx=15)

        # align inputs
        # l4.grid(row=1, column=0)
        # e1.grid(row=0, column=1)
        # e2.grid(row=1, column=1)
