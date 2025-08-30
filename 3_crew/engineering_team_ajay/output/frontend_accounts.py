#```python
import gradio as gr
from accounts import Account, get_share_price

class TradingPlatform:
    def __init__(self):
        self.accounts = {}

    def create_account(self, user_id, initial_deposit):
        account = Account(user_id)
        account.create_account(initial_deposit)
        self.accounts[user_id] = account
        return f"Account created for {user_id} with initial deposit of {initial_deposit}."

    def deposit(self, user_id, amount):
        account = self.accounts[user_id]
        account.deposit(amount)
        return f"Deposited {amount}. New balance: {account.balance:.2f}."

    def withdraw(self, user_id, amount):
        account = self.accounts[user_id]
        account.withdraw(amount)
        return f"Withdrew {amount}. New balance: {account.balance:.2f}."

    def buy_shares(self, user_id, symbol, quantity):
        account = self.accounts[user_id]
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}. New portfolio: {account.get_holdings()}."

    def sell_shares(self, user_id, symbol, quantity):
        account = self.accounts[user_id]
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}. New portfolio: {account.get_holdings()}."

    def get_portfolio_value(self, user_id):
        account = self.accounts[user_id]
        return f"Portfolio value: {account.portfolio_value():.2f}."

    def get_profit_loss(self, user_id):
        account = self.accounts[user_id]
        return f"Profit/Loss: {account.profit_loss():.2f}."

    def get_holdings(self, user_id):
        account = self.accounts[user_id]
        return f"Current holdings: {account.get_holdings()}."

    def get_transactions(self, user_id):
        account = self.accounts[user_id]
        return f"Transactions: {account.get_transactions()}."

def main():
    platform = TradingPlatform()

    with gr.Blocks() as demo:
        gr.Markdown("# Trading Simulation Platform")
        user_id = gr.Textbox(label="User ID", placeholder="Enter your User ID")
        initial_deposit = gr.Number(label="Initial Deposit", value=0.0)
        create_btn = gr.Button("Create Account")
        
        transaction_column = gr.Column()
        deposit_amount = gr.Number(label="Deposit Amount", value=0.0)
        withdraw_amount = gr.Number(label="Withdraw Amount", value=0.0)
        buy_symbol = gr.Textbox(label="Stock Symbol (e.g., AAPL)")
        buy_quantity = gr.Number(label="Buy Quantity", value=0)
        sell_symbol = gr.Textbox(label="Stock Symbol (e.g., AAPL)")
        sell_quantity = gr.Number(label="Sell Quantity", value=0)

        create_output = gr.Textbox(label="Create Account Output")
        deposit_output = gr.Textbox(label="Deposit Output")
        withdraw_output = gr.Textbox(label="Withdraw Output")
        buy_output = gr.Textbox(label="Buy Output")
        sell_output = gr.Textbox(label="Sell Output")
        portfolio_output = gr.Textbox(label="Portfolio Value Output")
        profit_loss_output = gr.Textbox(label="Profit/Loss Output")
        holdings_output = gr.Textbox(label="Holdings Output")
        transactions_output = gr.Textbox(label="Transactions Output")

        create_btn.click(
            lambda uid, dep: platform.create_account(uid, dep),
            inputs=[user_id, initial_deposit],
            outputs=create_output
        )
        
        deposit_btn = gr.Button("Deposit")
        deposit_btn.click(
            lambda uid, amt: platform.deposit(uid, amt),
            inputs=[user_id, deposit_amount],
            outputs=deposit_output
        )

        withdraw_btn = gr.Button("Withdraw")
        withdraw_btn.click(
            lambda uid, amt: platform.withdraw(uid, amt),
            inputs=[user_id, withdraw_amount],
            outputs=withdraw_output
        )

        buy_btn = gr.Button("Buy Shares")
        buy_btn.click(
            lambda uid, sym, qty: platform.buy_shares(uid, sym, qty),
            inputs=[user_id, buy_symbol, buy_quantity],
            outputs=buy_output
        )

        sell_btn = gr.Button("Sell Shares")
        sell_btn.click(
            lambda uid, sym, qty: platform.sell_shares(uid, sym, qty),
            inputs=[user_id, sell_symbol, sell_quantity],
            outputs=sell_output
        )

        portfolio_btn = gr.Button("Get Portfolio Value")
        portfolio_btn.click(
            lambda uid: platform.get_portfolio_value(uid),
            inputs=[user_id],
            outputs=portfolio_output
        )

        profit_loss_btn = gr.Button("Get Profit/Loss")
        profit_loss_btn.click(
            lambda uid: platform.get_profit_loss(uid),
            inputs=[user_id],
            outputs=profit_loss_output
        )

        holdings_btn = gr.Button("Get Holdings")
        holdings_btn.click(
            lambda uid: platform.get_holdings(uid),
            inputs=[user_id],
            outputs=holdings_output
        )

        transactions_btn = gr.Button("Get Transactions")
        transactions_btn.click(
            lambda uid: platform.get_transactions(uid),
            inputs=[user_id],
            outputs=transactions_output
        )

    demo.launch()

if __name__ == "__main__":
    main()
#```