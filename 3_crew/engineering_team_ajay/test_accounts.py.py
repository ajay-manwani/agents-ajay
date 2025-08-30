```python
import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('test_user')

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 0.0)

    def test_deposit(self):
        self.account.deposit(100.0)
        self.assertEqual(self.account.balance, 100.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0], ('Deposit', 100.0))

    def test_deposit_negative_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-50.0)

    def test_withdraw(self):
        self.account.deposit(100.0)
        self.account.withdraw(50.0)
        self.assertEqual(self.account.balance, 50.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1], ('Withdraw', 50.0))

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(50.0)

    def test_buy_shares(self):
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.balance, 700.0)
        self.assertEqual(self.account.portfolio['AAPL'], 2)
        self.assertEqual(len(self.account.transactions), 3)
        self.assertEqual(self.account.transactions[2], ('Buy', 'AAPL', 2))

    def test_buy_shares_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 10)

    def test_sell_shares(self):
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 2)
        self.account.sell_shares('AAPL', 1)
        self.assertEqual(self.account.balance, 850.0)
        self.assertEqual(self.account.portfolio['AAPL'], 1)
        self.assertEqual(len(self.account.transactions), 4)
        self.assertEqual(self.account.transactions[3], ('Sell', 'AAPL', 1))

    def test_sell_shares_insufficient_quantity(self):
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 2)
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 3)

    def test_calculate_portfolio_value(self):
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.calculate_portfolio_value(), 700.0)

    def test_report_holdings(self):
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.report_holdings(), {'AAPL': 2})

    def test_list_transactions(self):
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 2)
        transactions = self.account.list_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertIn(('Deposit', 1000.0), transactions)
        self.assertIn(('Buy', 'AAPL', 2), transactions)

if __name__ == '__main__':
    unittest.main()
```