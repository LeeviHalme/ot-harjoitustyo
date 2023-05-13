import tkinter
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkInputDialog
from utils.connect_database import get_database_connection
from repositories.budget_repository import BudgetRepository


class BudgetsView:
    """Class used to show budget list view

    Attributes:
        window (Ctk):                   CustomTkInter Main Window
        frame (CtkFrame | None):        Root frame for this view
        user (User):                    User in session

        view_budget (function):         Show BudgetSummaryView with given UID
        logout (function):              Method to log user out
        repack (function):              Repack the frame (destroy and pack)

        repository (BudgetRepository):  Budget repository instance
    """

    def __init__(self, window, view_budget, user, logout, repack) -> None:
        self.window = window
        self.frame = None
        self.user = user

        # methods
        self.view_budget = view_budget
        self.logout = logout
        self.repack = repack

        # declare repositories
        connection = get_database_connection()
        self.repository = BudgetRepository(connection)

        self.init()

    def pack(self):
        """Pack (use grid) the current frame into the window"""
        self.frame.grid(row=0, column=0, sticky="nsew")

    def destroy(self):
        """Destroy current frame"""
        self.frame.destroy()

    def prompt_name(self) -> str:
        """Prompt the user to enter a name

        Returns:
            string | None: Name from the popup
        """
        # prompt budget name
        name_dialog = CTkInputDialog(
            text="Syötä luotavan budjetin nimi (max 50 merkkiä):",
            title="Luo budjetti - Syötä nimi",
        )

        return name_dialog.get_input() or None

    def prompt_description(self) -> str:
        """Prompt the user to enter a description

        Returns:
            string | None: Description from the popup
        """
        description_dialog = CTkInputDialog(
            text="Syötä luotavan budjetin kuvaus (max 100 merkkiä):",
            title="Luo budjetti - Syötä kuvaus",
        )

        return description_dialog.get_input() or None

    def create_budget_prompt(self):
        """Button click handler for creating a new budget.
        Prompt's the user for two inputs (name and description)"""
        # get prompt values
        name = self.prompt_name()
        description = self.prompt_description()

        if not name or not description:
            tkinter.messagebox.showinfo(
                title="Hups!", message="Nimi tai kuvaus eivät saa olla tyhjiä"
            )
            return

        # create new budget
        self.repository.create_budget(name, description, self.user.id)

        # re-render the view in order to show new budget
        self.repack()

        # show success msg
        tkinter.messagebox.showinfo(
            title="Onnistui!",
            message=f"Budjetti luotu onnistuneesti! Nimi: {name}",
        )

    def init(self):
        """Main method to draw and initiate the view"""
        self.frame = CTkFrame(self.window, fg_color="transparent")

        # configure layout
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=2)
        self.frame.rowconfigure(2, weight=1)

        # create navbar
        f1 = CTkFrame(self.frame, fg_color="#dae8fc", height=50)
        f1.rowconfigure(0, weight=1)
        f1.columnconfigure(0, weight=1)
        f1.columnconfigure(1, weight=1)
        l1 = CTkLabel(
            f1,
            text=f"Kirjautuneena sisään käyttäjänä: @{self.user.username} ({self.user.name})",
            text_color="black",
        )
        b1 = CTkButton(f1, text="Kirjaudu Ulos", fg_color="gray", command=self.logout)
        l1.grid(row=0, column=0, sticky="w", padx=(20, 0))
        b1.grid(row=0, column=3, sticky="e", pady=15, padx=(0, 20))
        f1.grid(row=0, column=0, sticky="nwe")

        user_budgets = self.repository.get_user_budgets(self.user.id)

        # create budgets container
        f2 = CTkFrame(self.frame, fg_color="transparent")
        f2.columnconfigure(0, weight=1)

        # if user doesn't have budgets
        if len(user_budgets) == 0:
            lx = CTkLabel(
                f2,
                text='Sinulla ei ole budjetteja, luo uusi budjetti napauttamalla "Luo uusi".',
                text_color="gray",
            )
            lx.grid(row=0, column=0, sticky="ns")
        else:
            # create budget labels
            for index, budget in enumerate(user_budgets):
                # add row to container
                f2.rowconfigure(index, weight=1)

                # create frame for budget
                fx = CTkFrame(f2)
                fx.columnconfigure(0, weight=1)
                fx.columnconfigure(1, weight=1)
                fx.rowconfigure(0, weight=1)
                lx = CTkLabel(fx, text=budget.name)

                bx = CTkButton(
                    fx,
                    text="Avaa →",
                    command=lambda b_id=budget.id: self.view_budget(b_id),
                )
                lx.grid(row=0, column=0, pady=15, sticky="w", padx=(20, 0))
                bx.grid(row=0, column=1, sticky="e", pady=15, padx=(0, 20))
                fx.grid(row=index, column=0, sticky="nwe")

        f2.grid(row=1, column=0, sticky="nswe", padx=200)

        # create new-budget button
        f3 = CTkFrame(self.frame, height=50)
        b2 = CTkButton(f3, text="Luo uusi", command=self.create_budget_prompt)
        b2.grid(row=0, column=0)
        f3.grid(row=2, column=0)
