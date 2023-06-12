
from datetime import datetime


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class Acc_holder(User):
    def __init__(self, name, email, address, initial_deposit):
        super().__init__(name, email)
        self.address = address
        self.balance = initial_deposit
        self.loaned = 0
        self.transaction_history = []

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount > 0:
                self.balance += amount
                self.record_transaction("Deposit", amount)
                print(f"Successfully deposited {amount} into your account.")
            else:
                print("Deposit amount must be a positive number.")
        except ValueError:
            print("Invalid amount. Please provide a valid number.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be a positive number.")
        elif self.balance >= amount:
            self.balance -= amount
            self.record_transaction("Withdrawal", amount)
            print(f"Withdrawal of {amount} successful.")
        else:
            print("Insufficient balance.")

    def check_balance(self):
        print(f"Hello {self.name},")
        print(f"Your Balance: {self.balance}")

    def transfer_balance(self, amount, recipient):
        if amount <= 0:
            print("Transfer amount must be a positive number.")
        elif self.balance >= amount:
            self.balance -= amount
            recipient.balance += amount
            self.record_transaction("Transfer", amount)
            recipient.record_transaction("Received", amount)
            print(f"Successfully transferred {amount} to {recipient.name}.")
        else:
            print("Insufficient balance. Please refill your account.")

    def take_loan(self, amount, bank):
        if bank.get_loan_application_status():
            if self.loaned == 0 and amount <= 2 * self.balance:
                self.loaned = amount
                self.record_transaction("Loan", amount)
                print(f"{amount} added to your account as a loan successfully")
            else:
                print(f"You can't request a loan  {2 * self.balance}")
        else:
            print(f"Dear {self.name}, loan applications are not being accepted.")

    def record_transaction(self, rr_type, amount):
        transaction = {
            "type": rr_type,
            "amount": amount,
            "time": datetime.now().strftime("%H:%M:%S"),
        }
        self.transaction_history.append(transaction)

    def see_transaction_history(self):
        print(f"Hello {self.name},\nYour transaction details are:\n")
        for transaction in self.transaction_history:
            tr = f"- Type: {transaction['type']}, Amount: {transaction['amount']}, Time: {transaction['time']}"
            print(tr)

    def __repr__(self):
        acc_holder_details = f"Name: {self.name}\n"
        acc_holder_details += f"Balance: {self.balance}\n"
        return acc_holder_details


class Admin(User):
    def __init__(self, name, email, password):
        super().__init__(name, email)
        self.password = password

    def bank_create_new_account(self, account, bank):
        bank.create_new_account(account)

    def total_bank_balance(self, bank):
        return bank.total_bank_balance()

    def total_loan(self, bank):
        return bank.total_loan_given()

    def bank_toggle_loan_on_off(self, bank, password):
        bank.toggle_loan_on_off(password)


class Bank:
    acc_number_start = 1100
    loan_application_open = True

    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.admins = {}

    def create_new_account(self, account):
        account_number = self.generate_acc_no()
        self.accounts[account_number] = account

    def generate_acc_no(self):
        self.acc_number_start += 1
        return self.acc_number_start

    def _update_total_balance(self):
        return sum(acc.balance for acc in self.accounts.values())

    def _update_total_loan(self):
        return sum(acc.loaned for acc in self.accounts.values())

    def total_bank_balance(self):
        return self._update_total_balance()

    def total_loan_given(self):
        return self._update_total_loan()

    def net_balance(self):
        return self.total_bank_balance() - self.total_loan_given()

    def toggle_loan_on_off(self, password):
        admin = self.admins.get(password)
        if admin:
            self.loan_application_open = not self.loan_application_open
            print(
                "Loan feature has been enabled."
                if self.loan_application_open
                else "Loan feature has been disabled."
            )
        else:
            print("Invalid admin password.")

    def get_loan_application_status(self):
        return self.loan_application_open

    def __repr__(self):
        acc_details = f"Bank: {self.name}\n"
        acc_details += "---------------------------\n"
        for acc_no, acc in self.accounts.items():
            acc_details += f"Account Number: {acc_no}\n"
            acc_details += f"Account Details:\n{acc}\n"
        return acc_details


aulad_22 = Bank("aulad_22")
jweal = Acc_holder("jweal khan", "jweal22@.com", "bhola ", 600)
nazim = Acc_holder("nazim khan", "nazim22@.com", "Bhola", 500)
nazma = Acc_holder("nazma begum", "nazma34@.com", "Dhaka", 400)
zakia = Acc_holder('zakia kahn', 'zakia56@.com', 'barisal', 750)
aulad_22.create_new_account(jweal)
aulad_22.create_new_account(nazim)
aulad_22.create_new_account(nazma)
aulad_22.create_new_account(zakia)
jweal.deposit(5000)
jweal.check_balance()
jweal.transfer_balance(500, nazim)
jweal.transfer_balance(1500, nazim)
jweal.check_balance()
nazim.take_loan(1500, aulad_22)
nazim.check_balance()
jweal.see_transaction_history()
nazim.see_transaction_history()
nazim.withdraw(1000)
password = "password"
admin = Admin("admin", "adminkuja@.com", password)
aulad_22.admins[password] = admin
aulad_22.toggle_loan_on_off(password)
nazim.take_loan(1500, aulad_22)
