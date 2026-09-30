from abc import ABC, abstractmethod

class BankAccount(ABC):

    def __init__(self, account_number, account_holder, balance):
        self._account_number = account_number
        self._account_holder = account_holder
        self._balance = balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposited ₦{amount}")

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def calculate_interest(self):
        pass

    def get_balance(self):
        return self._balance



class SavingsAccount(BankAccount):

    INTEREST_RATE = 0.05

    def withdraw(self, amount):

        if amount <= self._balance:
            self._balance -= amount
            print("Withdrawal successful")
            return True

        else:
            print("Insufficient funds")
            return False

    def calculate_interest(self):

        interest = self._balance * self.INTEREST_RATE

        return interest
    


class CurrentAccount(BankAccount):

    OVERDRAFT_LIMIT = 5000

    def withdraw(self, amount):

        if self._balance + self.OVERDRAFT_LIMIT >= amount:

            self._balance -= amount
            print("Withdrawal successful")
            return True

        else:

            print("Overdraft exceeded")
            return False

    def calculate_interest(self):

        return 0