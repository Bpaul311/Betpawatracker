import csv
import os
from datetime import datetime

FILE_NAME = "betpawa_transactions.csv"

# Ensure the file exists with headers
def initialize_csv():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Type", "Amount", "Balance", "Daily Profit/Loss"])

# Get the latest balance
def get_balance():
    try:
        with open(FILE_NAME, mode='r') as file:
            reader = list(csv.reader(file))
            if len(reader) > 1:
                return float(reader[-1][3])  # Last balance value
    except Exception as e:
        print("Error reading balance:", e)
    return 0.0

# Get daily profit/loss
def get_daily_profit_loss():
    today = datetime.now().strftime("%Y-%m-%d")
    profit_loss = 0.0
    try:
        with open(FILE_NAME, mode='r') as file:
            reader = list(csv.reader(file))
            for row in reader[1:]:  # Skip header
                if today in row[0]:
                    profit_loss += float(row[2]) if row[1] == "deposit" else -float(row[2])
    except Exception as e:
        print("Error calculating daily profit/loss:", e)
    return profit_loss

# Log a transaction
def log_transaction(transaction_type, amount):
    balance = get_balance()
    if transaction_type == "withdraw" and amount > balance:
        print("Insufficient funds!")
        return
    
    new_balance = balance + amount if transaction_type == "deposit" else balance - amount
    daily_profit_loss = get_daily_profit_loss() + (amount if transaction_type == "deposit" else -amount)
    
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), transaction_type, amount, new_balance, daily_profit_loss])
    
    print(f"{transaction_type.capitalize()} of {amount} recorded. New balance: {new_balance}. Daily Profit/Loss: {daily_profit_loss}")

# Display transaction history
def view_transactions():
    try:
        with open(FILE_NAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(" | ".join(row))
    except Exception as e:
        print("Error reading file:", e)

def main():
    initialize_csv()
    while True:
        print("\n1. Deposit\n2. Withdraw\n3. View Transactions\n4. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            amount = float(input("Enter deposit amount: "))
            log_transaction("deposit", amount)
        elif choice == "2":
            amount = float(input("Enter withdrawal amount: "))
            log_transaction("withdraw", amount)
        elif choice == "3":
            view_transactions()
        elif choice == "4":
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
