import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account(user_id='user_123')

    def test_create_account_success(self):
        self.account.create_account(100.0)
        self.assertEqual(self.account.balance, 100.0)
        self.assertEqual(self.account.initial_deposit, 100.0)

    def test_create_account_with_zero_deposit(self):
        with self.assertRaises(ValueError):
            self.account.create_account(0)

    def test_create_account_with_negative_deposit(self):
        with self.assertRaises(ValueError):
            self.account.create_account(-50)

    def test_deposit_success(self):
        self.account.create_account(100.0)
        self.account.deposit(50.0)
        self.assertEqual(self.account.balance, 150.0)

    def test_deposit_with_zero_amount(self):
        self.account.create_account(100.0)
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    def test_deposit_with_negative_amount(self):
        self.account.create_account(100.0)
        with self.assertRaises(ValueError):
            self.account.deposit(-25)

    def test_withdraw_success(self):
        self.account.create_account(100.0)
        self.account.withdraw(50.0)
        self.assertEqual(self.account.balance, 50.0)

    def test_withdraw_insufficient_funds(self):
        self.account.create_account(100.0)
        with self.assertRaises(ValueError):
            self.account.withdraw(150.0)

    def test_withdraw_with_zero_amount(self):
        self.account.create_account(100.0)
        with self.assertRaises(ValueError):
            self.account.withdraw(0)

    def test_withdraw_with_negative_amount(self):
        self.account.create_account(100.0)
        with self.assertRaises(ValueError):
            self.account.withdraw(-50)

    def test_buy_shares_success(self):
        self.account.create_account(1000.0)
        self.account.buy_shares('AAPL', 5)
        self.assertEqual(self.account.balance, 1000.0 - (5 * 150.0))
        self.assertEqual(self.account.portfolio['AAPL'], 5)

    def test_buy_shares_insufficient_funds(self):
        self.account.create_account(100.0)
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 1)

    def test_buy_shares_invalid_quantity(self):
        self.account.create_account(1000.0)
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 0)

    def test_sell_shares_success(self):
        self.account.create_account(1000.0)
        self.account.buy_shares('AAPL', 5)
        self.account.sell_shares('AAPL', 5)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertNotIn('AAPL', self.account.portfolio)

    def test_sell_shares_insufficient(self):
        self.account.create_account(1000.0)
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 1)

    def test_sell_shares_invalid_quantity(self):
        self.account.create_account(1000.0)
        self.account.buy_shares('AAPL', 5)
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 0)

    def test_portfolio_value(self):
        self.account.create_account(1000.0)
        self.account.buy_shares('AAPL', 5)
        self.assertEqual(self.account.portfolio_value(), 1000.0 - (5 * 150.0))

    def test_profit_loss(self):
        self.account.create_account(1000.0)
        self.account.buy_shares('AAPL', 5)
        pl = self.account.profit_loss()
        self.assertAlmostEqual(pl, (-5 * 150.0))

    def test_get_holdings(self):
        self.account.create_account(1000.0)
        self.account.buy_shares('AAPL', 5)
        self.assertEqual(self.account.get_holdings(), {'AAPL': 5})

    def test_get_transactions(self):
        self.account.create_account(100.0)
        self.account.deposit(50.0)
        transactions = self.account.get_transactions()
        self.assertIn('Account created with initial deposit of 100.0.', transactions)
        self.assertIn('Deposited 50.0.', transactions)

if __name__ == '__main__':
    unittest.main()