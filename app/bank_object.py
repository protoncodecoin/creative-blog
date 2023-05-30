import sys
from bank_acount import BankAccount

oBank = BankAccount(300)

while True:
    print("Welcome to the ice bank")
    print("d - to deposit")
    print("w - to withdraw")
    print("b - to get balance")

    user_input = input("choose an option: ")
    user_input = user_input[0]

    if user_input == "d":
        print("** deposit **")
        amount = int(input("Enter the amount: "))
        oBank.deposit(amount)

    if user_input == "w":
        print("** withdraw **")
        amount = int(input("Enter amount: "))
        oBank.withdraw(amount)

    if user_input == "b":
        print("** Balance **")
        oBank.balance()

    if user_input == "q":
        break
