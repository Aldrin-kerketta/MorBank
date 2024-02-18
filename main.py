import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

conn = sqlite3.connect('bank_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        balance REAL DEFAULT 0.0
    )
''')
conn.commit()

def create_account(username, password):
    cursor.execute('INSERT INTO accounts (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    messagebox.showinfo("Success", "Account created successfully!")


# Function to perform a transaction (deposit/withdraw)
def perform_transaction(username, amount, transaction_type):
    cursor.execute('SELECT balance FROM accounts WHERE username = ?', (username,))
    current_balance = cursor.fetchone()[0]

    if transaction_type == 'Deposit':
        new_balance = current_balance + amount
    elif transaction_type == 'Withdraw':
        new_balance = current_balance - amount

    cursor.execute('UPDATE accounts SET balance = ? WHERE username = ?', (new_balance, username))
    conn.commit()
    messagebox.showinfo("Success", f"{transaction_type} successful!\nNew balance: {new_balance}")


# Function to handle login
def login(username, password):
    cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (username, password))
    account = cursor.fetchone()

    if account:
        logged_in_menu(account[0])
    else:
        messagebox.showerror("Error", "Invalid credentials")


# Function to display the main menu after logging in
def logged_in_menu(account_id):
    account_window = tk.Toplevel(root)
    account_window.title("Bank Application")
    account_window.geometry("300x300")
    # Create GUI elements for the main menu
    label = tk.Label(account_window, text=f"Welcome, Account #{account_id}")
    label.pack(pady=10)

    deposit_button = tk.Button(account_window, text="Deposit",
                               command=lambda: perform_transaction(account_id, get_amount(), 'Deposit'))
    deposit_button.pack(pady=10)

    withdraw_button = tk.Button(account_window, text="Withdraw",
                                command=lambda: perform_transaction(account_id, get_amount(), 'Withdraw'))
    withdraw_button.pack(pady=10)


# Function to get the transaction amount from the user
def get_amount():
    amount = simpledialog.askfloat("Amount", "Enter amount:")
    return amount


# Function to handle account creation
def create_account_menu():
    create_account_window = tk.Toplevel(root)
    create_account_window.title("Create Account")
    create_account_window.geometry("300x300")

    label = tk.Label(create_account_window, text="Create Account")
    label.pack(pady=10)

    username_label = tk.Label(create_account_window, text="Username:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(create_account_window)
    username_entry.pack(pady=5)

    password_label = tk.Label(create_account_window, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(create_account_window, show="*")
    password_entry.pack(pady=5)

    create_button = tk.Button(create_account_window, text="Create Account",
                              command=lambda: create_account(username_entry.get(), password_entry.get()))
    create_button.pack(pady=10)


# Function to handle login menu
def login_menu():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x300")

    label = tk.Label(login_window, text="Login")
    label.pack(pady=10)

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(login_window, text="Login",
                             command=lambda: login(username_entry.get(), password_entry.get()))
    login_button.pack(pady=10)


# Main GUI window
root = tk.Tk()
root.title("Bank Application")
root.geometry("300x300")

# Create GUI elements for the main window

create_account_button = tk.Button(root, text="Create Account", command=create_account_menu)
create_account_button.pack(pady=10)

login_button = tk.Button(root, text="Login", command=login_menu)
login_button.pack(pady=10)

# Run the main loop
root.mainloop()
