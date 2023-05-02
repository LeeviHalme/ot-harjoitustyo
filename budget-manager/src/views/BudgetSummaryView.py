import tkinter
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkButton,
    CTkInputDialog,
    CTkScrollableFrame,
)
from utils.connect_database import get_database_connection
from repositories.BudgetRepository import BudgetRepository


class BudgetSummaryView:
    def __init__(self, window, user, logout, show_budgets, repack, budget_id) -> None:
        self.window = window
        self.frame = None
        self.user = user
        self.budget_id = budget_id
        self.budget = None

        # methods
        self.logout = logout
        self.show_budgets = show_budgets
        self.repack = repack

        # declare repositories
        connection = get_database_connection()
        self.repository = BudgetRepository(connection)

        # declare state
        self.username_entry = None

        self.init()

    def pack(self):
        self.frame.grid(row=0, column=0, sticky="nsew")

    def destroy(self):
        self.frame.destroy()

    def prompt_name(self):
        # prompt budget name
        name_dialog = CTkInputDialog(
            text="Syötä uusi nimi (max 50 merkkiä):",
            title=f"Muokkaa budjettia {self.budget.name} - Syötä nimi",
        )

        return name_dialog.get_input() or None

    def prompt_description(self):
        description_dialog = CTkInputDialog(
            text="Syötä uusi kuvaus (max 100 merkkiä):",
            title=f"Muokkaa budjettia {self.budget.name} - Syötä kuvaus",
        )

        return description_dialog.get_input() or None

    # enter new values for budget
    def edit_budget(self):
        if not self.budget:
            return

        # prompt values
        name = self.prompt_name()
        description = self.prompt_description()

        if not name or not description:
            tkinter.messagebox.showinfo(
                title="Hups!", message="Nimi tai kuvaus eivät saa olla tyhjiä"
            )
            return

        # TODO: Validate input

        # update budget
        success = self.repository.update_budget(self.budget.id, name, description)
        if not success:
            tkinter.messagebox.showerror(
                title="Hups!", message="Budjetin päivittämisessä tapahtui virhe."
            )
        else:
            tkinter.messagebox.showinfo(
                title="Budjetti päivitetty!", message="Budjetin päivittäminen onnistui."
            )

        # update class budget reference
        self.budget.name = name
        self.budget.description = description

        # refresh view
        self.repack()

    def init(self):
        self.frame = CTkFrame(self.window, fg_color="transparent")

        # get budget by id
        self.budget = self.repository.get_budget_by_id(self.budget_id)

        # configure layout
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=1)

        # create navbar
        f1 = CTkFrame(self.frame, fg_color="#dae8fc")
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

        # create view container
        f2 = CTkFrame(self.frame, fg_color="transparent")
        f2.rowconfigure(0, weight=1)
        f2.columnconfigure(0, weight=1)
        f2.columnconfigure(1, weight=1)
        f2.grid(row=1, column=0, sticky="nswe")

        # create right side
        f3 = CTkFrame(f2, fg_color="transparent")
        f3.rowconfigure(0, weight=1)
        f3.rowconfigure(1, weight=1)
        f3.columnconfigure(0, weight=1)
        f3.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)

        # create title and desc
        f4 = CTkFrame(f3, fg_color="transparent")
        f4.rowconfigure(0, weight=1)
        f4.rowconfigure(1, weight=1)
        f4.rowconfigure(2, weight=1)
        f4.rowconfigure(3, weight=1)
        f4.columnconfigure(0, weight=1)
        b2 = CTkButton(f4, text="← Takaisin", command=self.show_budgets)
        l2 = CTkLabel(f4, text=self.budget.name, font=("Arial", 22, "bold"))
        l3 = CTkLabel(
            f4,
            text=self.budget.description,
            wraplength=300,
            font=("Monospace", 18),
            justify="left",
        )
        l4 = CTkLabel(
            f4,
            text=f"Budjetin ID: {self.budget.id}",
            font=("Monospace", 10),
            justify="left",
        )
        b2.grid(row=0, column=0, sticky="w", pady=(0, 20))
        l2.grid(row=1, column=0, sticky="w")
        l3.grid(row=2, column=0, sticky="w")
        l4.grid(row=3, column=0, sticky="w")
        f4.grid(row=0, column=0, sticky="n")

        # create budget control buttons
        f5 = CTkFrame(f3)
        f4.columnconfigure(0, weight=1)
        f4.rowconfigure(0, weight=1)
        f4.rowconfigure(1, weight=1)
        f4.rowconfigure(2, weight=1)
        f4.rowconfigure(3, weight=1)
        b3 = CTkButton(f5, text="Muuta budjetin tietoja", command=self.edit_budget)
        b4 = CTkButton(
            f5,
            text="Muuta menoja/tuloja/kuluja (tulossa)",
            fg_color="gray",
            state="disabled",
        )
        b5 = CTkButton(
            f5,
            text="Jaa budjetti käyttäjälle (tulossa)",
            fg_color="gray",
            state="disabled",
        )
        b6 = CTkButton(
            f5, text="Poista budjetti", fg_color="red", hover_color="indian red"
        )
        b3.grid(row=0, column=0, sticky="nwes", padx=15, pady=15)
        b4.grid(row=1, column=0, sticky="nwes", padx=15, pady=(0, 15))
        b5.grid(row=2, column=0, sticky="nwes", padx=15)
        b6.grid(row=3, column=0, sticky="nwes", padx=15, pady=15)
        f5.grid(row=1, column=0, sticky="wn")

        # create left side
        f6 = CTkFrame(f2, fg_color="transparent")
        f6.columnconfigure(0, weight=1)
        f6.rowconfigure(0, weight=0)
        f6.rowconfigure(1, weight=1)
        f6.grid(row=0, column=1, sticky="nsew")

        # create info boxes
        f7 = CTkFrame(f6, fg_color="transparent")
        f7.columnconfigure(0, weight=1)
        f7.rowconfigure(0, weight=0)
        f7.rowconfigure(1, weight=0)
        f7.grid(row=0, column=0, sticky="wne")

        # create top box
        f8 = CTkFrame(f7)
        f8.columnconfigure(0, weight=1)
        f8.rowconfigure(0, weight=1)
        f8.rowconfigure(1, weight=2)
        l5 = CTkLabel(f8, text="Saldo")
        l6 = CTkLabel(f8, text="250.43 €", font=("Monospace", 30, "bold"))
        l5.grid(row=0, column=0)
        l6.grid(row=1, column=0, pady=(0, 10))
        f8.grid(row=0, column=0, padx=10, pady=(15, 10), sticky="nswe")

        # create secondary boxes
        f9 = CTkFrame(f7, fg_color="transparent")
        f9.columnconfigure(0, weight=1)
        f9.columnconfigure(1, weight=1)
        f9.rowconfigure(0, weight=1)
        f9.grid(row=1, column=0, sticky="we")

        # create box for income
        f10 = CTkFrame(f9)
        f10.columnconfigure(0, weight=1)
        f10.rowconfigure(0, weight=1)
        f10.rowconfigure(1, weight=2)
        l7 = CTkLabel(f10, text="Tulot")
        l8 = CTkLabel(
            f10, text="2456.32 €", text_color="green", font=("Monospace", 28, "bold")
        )
        l7.grid(row=0, column=0)
        l8.grid(row=1, column=0, pady=(0, 10))
        f10.grid(row=0, column=0, padx=(10, 5), sticky="we")

        # create box for expenses
        f11 = CTkFrame(f9)
        f11.columnconfigure(0, weight=1)
        f11.rowconfigure(0, weight=1)
        f11.rowconfigure(1, weight=2)
        l9 = CTkLabel(f11, text="Menot ja kulut")
        l10 = CTkLabel(
            f11,
            text="2205.89 €",
            text_color="indian red",
            font=("Monospace", 28, "bold"),
        )
        l9.grid(row=0, column=0)
        l10.grid(row=1, column=0, pady=(0, 10))
        f11.grid(row=0, column=1, padx=(5, 10), sticky="we")

        # create transactions table
        f12 = CTkFrame(f6)
        f12.columnconfigure(0, weight=1)
        f12.rowconfigure(0, weight=0)
        f12.rowconfigure(1, weight=1)
        sf = CTkScrollableFrame(f12)
        l11 = CTkLabel(f12, text="Kaikki tapahtumat päivämäärän mukaan")
        l11.grid(row=0, column=0, pady=5)
        f12.grid(row=1, column=0, pady=15, padx=10, sticky="nwse")

        transactions = []

        # check if no transactions
        if len(transactions) == 0:
            lx = CTkLabel(
                f12,
                text='Sinulla ei ole tapahtumia. Lisää tapahtumia painamalla "Muuta menoja/tuloja/kuluja"',
                text_color="gray",
                wraplength=200,
            )
            lx.grid(row=1, column=0)
        else:
            # TODO: create entry for each trx
            for index, trx in enumerate(transactions):
                lx = CTkLabel(sf, text="Test transaction")
                lx.grid(row=index, column=0)
            sf.grid(row=1, column=0, sticky="we")