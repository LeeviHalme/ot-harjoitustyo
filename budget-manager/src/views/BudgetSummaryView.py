import tkinter
import datetime
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
    """Class used to show budget summary view

    Attributes:
        window (Ctk):                   CustomTkInter Main Window
        frame (CtkFrame | None):        Root frame for this view
        user (User):                    User in session

        budget_id (str):                Currently viewed budget's UID
        budget (Budget | None):         Parsed budget object from DB

        logout (function):              Method to log user out
        show_budgets (function):        Show budgets view
        repack (function):              Repack the frame (destroy and pack)
        repository (BudgetRepository):  Budget repository instance
    """

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
            text="Syötä uusi nimi (max 50 merkkiä):",
            title=f"Muokkaa budjettia {self.budget.name} - Syötä nimi",
        )

        return name_dialog.get_input() or None

    def prompt_description(self) -> str:
        """Prompt the user to enter a description

        Returns:
            string | None: Description from the popup
        """
        description_dialog = CTkInputDialog(
            text="Syötä uusi kuvaus (max 100 merkkiä):",
            title=f"Muokkaa budjettia {self.budget.name} - Syötä kuvaus",
        )

        return description_dialog.get_input() or None

    # enter new values for budget
    def edit_budget(self):
        """Button click handler for editing the budget details"""
        if not self.budget:
            return

        # prompt values
        name = self.prompt_name()
        description = self.prompt_description()

        if not name or not description:
            tkinter.messagebox.showerror(
                title="Hups!", message="Nimi tai kuvaus eivät saa olla tyhjiä"
            )
            return

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

    def prompt_trx_name(self) -> str:
        """Prompt the user to enter a transaction name

        Returns:
            string | None: Name from the popup
        """
        # prompt transaction name
        name_dialog = CTkInputDialog(
            text="Syötä tapahtuman nimi (max 100 merkkiä):",
            title=f"Lisää tapahtuma - Syötä nimi",
        )

        return name_dialog.get_input() or None

    def prompt_trx_amount(self) -> str:
        """Prompt the user to enter transaction amount

        Returns:
            string | None: Amount from the popup
        """
        # prompt transaction amount
        amount_dialog = CTkInputDialog(
            text="Syötä tapahtuman arvo senteissä (esim. 15.50 € = 1550): HUOM: Jos kyseessä on meno/kulu ilmoita arvo negatiivisena (esim. -600 € = -60000):",
            title=f"Lisää tapahtuma - Syötä arvo",
        )

        return amount_dialog.get_input() or None

    def prompt_trx_due_date(self) -> str:
        """Prompt the user to enter transaction due date

        Returns:
            string | None: Amount from the popup
        """
        # prompt transaction due date
        date_dialog = CTkInputDialog(
            text="Syötä tapahtuman eräpäivä päivä.kk (esim. 20.5):",
            title=f"Lisää tapahtuma - Syötä eräpäivä",
        )

        return date_dialog.get_input() or None

    def _format_input_date(self, input_str: str) -> str:
        day_num, month_num = input_str.split(".")
        day = day_num if int(day_num) > 10 else f"0{day_num}"
        month = month_num if int(month_num) > 10 else f"0{month_num}"
        year = datetime.date.today().year
        return f"{year}-{month}-{day} 00:00:00"

    def _validate_date(self, input_str: str) -> bool:
        try:
            day_num, month_num = input_str.split(".")

            # if they are not digits
            if not day_num.isdigit() or not month_num.isdigit():
                return False

            formatted = self._format_input_date(input_str)

            datetime.datetime.strptime(formatted, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False

    def _validate_amount(self, input_str: str) -> bool:
        return input_str.isdigit() or (input_str[0] == "-" and input_str[1:].isdigit())

    def add_transaction(self):
        """Button click handler for adding a transaction"""
        if not self.budget:
            return

        # prompt values
        name = self.prompt_trx_name()
        amount = self.prompt_trx_amount()
        due_date = self.prompt_trx_due_date()

        if not name or not amount or not due_date:
            tkinter.messagebox.showerror(
                title="Hups!", message="Täytä huolellisesti kaikki kohdat!"
            )
            return

        # Validate input
        valid = True
        failed_field = ""
        if len(name) < 1 or len(name) > 100:
            valid = False
            failed_field = "nimi"
        elif not self._validate_amount(amount):
            valid = False
            failed_field = "arvo"
        elif not self._validate_date(due_date):
            valid = False
            failed_field = "eräpäivä"

        if not valid:
            tkinter.messagebox.showerror(
                title="Hups!",
                message=f"Täytä huolellisesti kaikki kohdat (validointivirhe kohdassa: {failed_field})!",
            )
            return

        # add the new transaction
        self.repository.add_transaction(
            name, amount, self._format_input_date(due_date), self.budget_id
        )

        # refresh view
        self.repack()

    def remove_trx(self, trx_id: str):
        """Remove a singular transaction by UID

        Args:
            trx_id (str): Transaction's UID to remove
        """

        success = self.repository.remove_transaction(trx_id)
        if success:
            tkinter.messagebox.showinfo(
                title="Onnistui!", message="Tapahtuma poistettu!"
            )

        # re-render the view in order to remove the trx
        self.repack()

    def remove_budget(self):
        """Prompt user to confirm deletion, and delete current budget"""

        # prompt user a yes / no
        result = tkinter.messagebox.askyesno(
            title="Vahvistus",
            message=f'Haluatko varmasti poistaa budjetin "{self.budget.name}"?',
        )
        if result:
            success = self.repository.remove_budget(self.budget_id)
            if success:
                tkinter.messagebox.showinfo(
                    title="Onnistui!", message="Budjetti poistettu onnistuneesti."
                )

                # redirect to budgets view
                self.show_budgets()

    def init(self):
        """Main method to draw and initiate the view"""
        self.frame = CTkFrame(self.window, fg_color="transparent")

        # get budget by id
        self.budget = self.repository.get_budget_by_id(self.budget_id)

        # get user current month transactions
        transactions = self.repository.get_current_month_transactions(self.budget_id)

        # get statistics about current month
        balance, income, outcome = self.repository.get_current_month_stats(
            self.budget_id
        )

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
            f5, text="Lisää meno / tulo / kulu", command=self.add_transaction
        )
        b5 = CTkButton(
            f5,
            text="Jaa budjetti käyttäjälle (tulossa)",
            fg_color="gray",
            state="disabled",
        )
        b6 = CTkButton(
            f5,
            text="Poista budjetti",
            fg_color="red",
            hover_color="indian red",
            command=self.remove_budget,
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
        l6 = CTkLabel(f8, text=f"{balance} €", font=("Monospace", 30, "bold"))
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
            f10, text=f"{income} €", text_color="green", font=("Monospace", 28, "bold")
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
            text=f"{outcome} €",
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
        sf.columnconfigure(0, weight=1)
        l11 = CTkLabel(f12, text="Kaikki tapahtumat päivämäärän mukaan")
        l11.grid(row=0, column=0, pady=5)
        f12.grid(row=1, column=0, pady=15, padx=10, sticky="nwse")

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
            # create entry for each trx
            for index, trx in enumerate(transactions):
                fx = CTkFrame(sf, fg_color="transparent")
                fx.rowconfigure(0, weight=1)
                fx.columnconfigure(0, weight=1)
                fx.columnconfigure(1, weight=1)
                fx.columnconfigure(2, weight=1)
                fx.columnconfigure(3, weight=0)

                amount = trx.get_amount()
                lx1 = CTkLabel(
                    fx,
                    text=f"+{amount}" if amount > 0 else amount,
                    text_color="red" if amount < 0 else "green",
                    justify="left",
                )

                lx2 = CTkLabel(fx, text=trx.name)
                lx3 = CTkLabel(
                    fx, text=trx.get_due_date(), text_color="gray", anchor="w"
                )
                bx = CTkButton(
                    fx,
                    text="Poista",
                    fg_color="transparent",
                    text_color="gray",
                    hover_color="indian red",
                    width=65,
                    command=lambda trx_id=trx.id: self.remove_trx(trx_id),
                )

                lx1.grid(row=0, column=0, sticky="w", padx=(10, 0))
                lx2.grid(row=0, column=1, padx=25, sticky="we")
                lx3.grid(row=0, column=2, sticky="we")
                bx.grid(row=0, column=3, sticky="e")
                fx.grid(row=index, column=0, sticky="we")
            sf.grid(row=1, column=0, sticky="we")
