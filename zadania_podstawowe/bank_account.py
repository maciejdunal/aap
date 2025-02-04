# Napisz klasę BankAccount, która implementuje podstawowe operacje na koncie
# bankowym, takie jak wpłacanie, wypłacanie i sprawdzanie salda. Klasa powinna
# wywoływać wyjątek przy próbie wpłaty lub wypłaty niepoprawnej kwoty.
# Następnie napisz testy jednostkowe za pomocą unittest, które sprawdzą
# poprawność działania metod oraz obsługę błędów

import logging

logging.basicConfig(level=logging.INFO)

class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    def get_balance(self):
        return self.balance