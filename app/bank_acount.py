class BankAccount:
    def __init__(self, amount):
        self.amount = amount

    def deposit(self, amount):
        """ Deposit into account"""
        amount = int(amount)
        if amount >= 0:
            self.amount += amount
        print(self.amount)
        return self.amount

    def withdraw(self, amount):
        """ Withdraw from bank account"""
        amount = int(amount)
        if amount <= self.amount:
            self.amount -= amount
        print(self.amount)
        return self.amount

    def balance(self):
        """ Check the balance """
        print(self.amount)
        return self.amount


