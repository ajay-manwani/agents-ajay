```python
import gradio as gr
from accounts import Account, get_share_price

# Global account dictionary to manage multiple users
accounts = {}

def create_account(user_id):
    """Function to create a new account."""
    if user_id in accounts:
        return "Account already exists."
    accounts[user_id] = Account(user_id)
    return f"Account created for {user_id}."

def deposit_funds(user_id, amount):
    """Function to deposit funds into an account."""
    account = accounts.get(user_id)
    if account is None:
        return "Account does not exist."
    try:
        account.deposit(amount)
        return f"Deposited ${amount} to {user_id}'s account. New balance: ${account.balance}."
    except ValueError as e:
        return str(e)

def withdraw_funds(user_id, amount):
    """Function to withdraw funds from an account."""
    account = accounts.get(user_id)
    if account is None:
        return "Account does not exist."
    try:
        account.withdraw(amount)
        return f"Withdrew ${amount} from {user_id}'s account. New balance: ${account.balance}."
    except ValueError as e:
        return str(e)

def buy_shares(user_id, symbol, quantity):
    """Function to buy shares."""
    account = accounts.get(user_id)
    if account is None:
        return "Account does not exist."
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol} for {user_id}."
    except ValueError as e:
        return str(e)

def sell_shares(user_id, symbol, quantity):
    """Function to sell shares."""
    account = accounts.get(user_id)
    if account is None:
        return "Account does not exist."
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol} for {user_id}."
    except ValueError as e:
        return str(e)

def portfolio_value(user_id):
    """Function to calculate the total value of the portfolio."""
    account = accounts.get(user_id)
    if account is None:
        return "Account does not exist."
    return f"Total portfolio value for {user_id}: ${account.calculate_portfolio_value()}."

def profit_loss(user_id):
    """Function to calculate profit or loss."""
    account = accounts.get(user_id)
    if account is None:
        return "Account does not exist."
    return f"Profit/Loss for {user_id}: ${account.calculate_profit_loss()}."

def report_holdings(user_id):
    """Function to report current holdings."""
    account = accounts.get(user_id)
    if account is None:
        return "Account does not exist."
    holdings = account.report_holdings()
    return f"Holdings for {user_id}: {holdings}."

def list_transactions(user_id):
    """Function to list all transactions."""
    account = accounts.get(user_id)
    if account is None:
        return "Account does not exist."
    transactions = account.list_transactions()
    return f"Transactions for {user_id}: {transactions}."

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("### Trading Account Management System")
    
    with gr.Tab("Account Operations"):
        user_id = gr.Textbox(label="User ID")
        create_btn = gr.Button("Create Account")
        deposit_input = gr.Number(label="Deposit Amount")
        deposit_btn = gr.Button("Deposit Funds")
        withdraw_input = gr.Number(label="Withdraw Amount")
        withdraw_btn = gr.Button("Withdraw Funds")
        
        create_output = gr.Textbox(label="Create Account Response", interactive=False)
        deposit_output = gr.Textbox(label="Deposit Response", interactive=False)
        withdraw_output = gr.Textbox(label="Withdraw Response", interactive=False)
        
        create_btn.click(create_account, inputs=user_id, outputs=create_output)
        deposit_btn.click(deposit_funds, inputs=[user_id, deposit_input], outputs=deposit_output)
        withdraw_btn.click(withdraw_funds, inputs=[user_id, withdraw_input], outputs=withdraw_output)
    
    with gr.Tab("Trading Operations"):
        buy_symbol = gr.Textbox(label="Stock Symbol to Buy")
        buy_quantity = gr.Number(label="Quantity")
        buy_btn = gr.Button("Buy Shares")
        sell_symbol = gr.Textbox(label="Stock Symbol to Sell")
        sell_quantity = gr.Number(label="Quantity")
        sell_btn = gr.Button("Sell Shares")
        
        buy_output = gr.Textbox(label="Buy Shares Response", interactive=False)
        sell_output = gr.Textbox(label="Sell Shares Response", interactive=False)
        
        buy_btn.click(buy_shares, inputs=[user_id, buy_symbol, buy_quantity], outputs=buy_output)
        sell_btn.click(sell_shares, inputs=[user_id, sell_symbol, sell_quantity], outputs=sell_output)
    
    with gr.Tab("Portfolio"):
        value_btn = gr.Button("Portfolio Value")
        profit_loss_btn = gr.Button("Profit or Loss")
        holdings_btn = gr.Button("Report Holdings")
        transactions_btn = gr.Button("List Transactions")
        
        value_output = gr.Textbox(label="Portfolio Value Response", interactive=False)
        profit_loss_output = gr.Textbox(label="Profit/Loss Response", interactive=False)
        holdings_output = gr.Textbox(label="Holdings Response", interactive=False)
        transactions_output = gr.Textbox(label="Transactions Response", interactive=False)
        
        value_btn.click(portfolio_value, inputs=user_id, outputs=value_output)
        profit_loss_btn.click(profit_loss, inputs=user_id, outputs=profit_loss_output)
        holdings_btn.click(report_holdings, inputs=user_id, outputs=holdings_output)
        transactions_btn.click(list_transactions, inputs=user_id, outputs=transactions_output)

demo.launch()
```