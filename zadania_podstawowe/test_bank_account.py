# Napisz klasę BankAccount, która implementuje podstawowe operacje na koncie
# bankowym, takie jak wpłacanie, wypłacanie i sprawdzanie salda. Klasa powinna
# wywoływać wyjątek przy próbie wpłaty lub wypłaty niepoprawnej kwoty.
# Następnie napisz testy jednostkowe za pomocą unittest, które sprawdzą
# poprawność działania metod oraz obsługę błędów

import unittest
from bank_account import BankAccount

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        """Tworzy nową instancję BankAccount przed każdym testem"""
        self.account = BankAccount(100)  # Konto z początkowym saldem 100
    
    def test_deposit(self):
        """Testuje poprawne wpłaty"""
        self.account.deposit(50)
        self.assertEqual(self.account.get_balance(), 150)

    def test_withdraw(self):
        """Testuje poprawne wypłaty"""
        self.account.withdraw(30)
        self.assertEqual(self.account.get_balance(), 70)

    def test_invalid_deposit(self):
        """Testuje próbę wpłaty ujemnej wartości"""
        with self.assertRaises(ValueError):
            self.account.deposit(-10)

    def test_overdraw(self):
        """Testuje próbę wypłaty większej kwoty niż dostępne saldo"""
        with self.assertRaises(ValueError):
            self.account.withdraw(200)

    def test_zero_deposit(self):
        """Testuje próbę wpłaty 0 zł - powinna zakończyć się błędem"""
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    def test_zero_withdraw(self):
        """Testuje próbę wypłaty 0 zł - powinna zakończyć się błędem"""
        with self.assertRaises(ValueError):
            self.account.withdraw(0)

if __name__ == "__main__":
    unittest.main()