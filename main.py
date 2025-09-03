import json
class Account:
    def __init__(self, name, balance):
        self.__name = name
        self.__balance = balance

    def __str__(self):
        return f"Name: {self.__name}, Balance: {self.__balance}"

    def get_name(self):
        return self.__name

    def get_balance(self):
        return self.__balance

    def set_balance(self, balance):
        self.__balance = balance

    def to_dict(self):
        return {"name": self.__name, "balance": self.__balance}

class BankSystem:
    __new_account_id = 0
    def __init__(self):
        self.__accounts = {}

    def save_accounts(self):
        try:
            with open("accounts.json", "w") as file:
                data = {account_id:account.to_dict() for account_id, account in self.__accounts.items()}
                json.dump(data, file, indent=4)
                print("Accounts successfully saved.")
        except PermissionError:
            print("You do not have permission to write to the file.")
        except TypeError:
            print("Data could not be serialized to JSON.")
        except OSError:
            print("File system error.")
        except Exception as e:
            print("Unexpected error:", e)

    def load_accounts(self):
        try:
            with open("accounts.json", "r") as file:
                data = json.load(file)
                max_id = -1
                for account_id, account in data.items():
                    self.__accounts[int(account_id)] = Account(account["name"], float(account["balance"]))
                    if int(account_id) > max_id:
                        max_id = int(account_id)
                self.__new_account_id = max_id + 1
                print("Accounts successfully loaded.")
        except FileNotFoundError:
            print("accounts.json could not found.")
        except PermissionError:
            print("You do not have permission to read from that file.")
        except OSError:
            print("File system error.")
        except Exception as e:
            print("Unexpected error:", e)

    def add_account(self, name, balance):
        self.__accounts[self.__new_account_id] = Account(name, balance)
        print(f"Account with ID {self.__new_account_id} successfully added.")
        self.__new_account_id += 1
        self.save_accounts()

    def delete_account(self, account_id):
        if account_id in self.__accounts:
            del self.__accounts[account_id]
            print(f"Account with ID {account_id} successfully deleted.")
            self.save_accounts()
        else:
            print(f"Account with ID {account_id} could not found.")

    def list_accounts(self):
        for account_id, account in self.__accounts.items():
            print(f"ID: {account_id}, {account}")

    def update_balance(self, account_id, amount):
        account = self.__accounts.get(account_id)
        if not account:
            print("Account not found.")
            return False

        new_balance = account.get_balance() + amount
        if new_balance < 0:
            print("Insufficient amount. Cannot complete the transaction.")
            return False

        account.set_balance(new_balance)
        return True

    def deposit(self, account_id, amount):
        if amount <= 0:
            print("Invalid amount for deposit.")
        elif self.update_balance(account_id, amount):
            print(f"{amount} deposited to account with ID {account_id}.")
            self.save_accounts()
            return True
        return False

    def withdraw(self, account_id ,amount):
        if amount <= 0:
            print("Invalid amount for withdraw.")
        elif self.update_balance(account_id, -amount):
            print(f"{amount} withdrawn from account with ID {account_id}")
            self.save_accounts()
            return True
        return False

    def transfer(self, sender_id, receiver_id, amount):
        if not self.withdraw(sender_id, amount):
            print("Transfer failed: insufficient balance or invalid sender ID.")
        elif not self.deposit(receiver_id, amount):
            print("Transfer failed: invalid receiver ID. Refunding sender.")
            self.deposit(sender_id, amount)
        else:
            print("Transfer successful.")

def get_float_safely(prompt):
    while True:
        try:
            number = float(input(prompt))
            return number
        except ValueError:
            print("Please enter a number.")
        except Exception as e:
            print("An error occurred:", e)


def get_int_safely(prompt):
    while True:
        try:
            number = int(input(prompt))
            return number
        except ValueError:
            print("Please enter a number.")
        except Exception as e:
            print("An error occurred:", e)


class BankMenu:
    def __init__(self):
        self.bank_system = BankSystem()

    def init_system(self):
        self.bank_system.load_accounts()

    def add_account_menu(self):
        name = input("Please enter the name >> ")
        balance = get_float_safely("Please enter the balance >> ")
        self.bank_system.add_account(name, balance)

    def delete_account_menu(self):
        account_id = get_int_safely("Please enter the account ID >> ")
        self.bank_system.delete_account(account_id)

    def deposit_menu(self):
        account_id = get_int_safely("Please enter the account ID >> ")
        amount = get_float_safely("Please enter the amount for deposit >> ")
        self.bank_system.deposit(account_id, amount)

    def withdraw_menu(self):
        account_id = get_int_safely("Please enter the account ID >> ")
        amount = get_float_safely("Please enter the amount for withdraw >> ")
        self.bank_system.withdraw(account_id, amount)

    def transfer_menu(self):
        sender_id = get_int_safely("Please enter the sender ID >> ")
        receiver_id = get_int_safely("Please enter the receiver ID >> ")
        amount = get_float_safely("Please enter the amount for transfer >> ")
        self.bank_system.transfer(sender_id, receiver_id, amount)

    def main_menu(self):
        print("Welcome! This is banking system by Suleyman Kara. Written in Python.")
        while True:
            print("\n1: Add Account",
                  "2: Delete Account",
                  "3: List Accounts",
                  "4: Deposit",
                  "5: Withdraw",
                  "6: Transfer",
                  "7: Exit", sep="\n")

            while True:
                try:
                    choice = int(input("Input >> "))
                    if 0 < choice < 8:
                        break
                    else:
                        print("Please enter an integer between 1-7.")
                except ValueError:
                    print("Please enter an integer.")
                except Exception as e:
                    print("An error occurred:", e)

            if choice == 1:
                self.add_account_menu()
            elif choice == 2:
                self.delete_account_menu()
            elif choice == 3:
                self.bank_system.list_accounts()
            elif choice == 4:
                self.deposit_menu()
            elif choice == 5:
                self.withdraw_menu()
            elif choice == 6:
                self.transfer_menu()
            elif choice == 7:
                self.bank_system.save_accounts()
                print("Goodbye!")
                return

def main():
    bank = BankMenu()
    bank.init_system()
    bank.main_menu()
    return

if __name__ == "__main__":
    main()