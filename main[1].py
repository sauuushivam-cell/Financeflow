import json
import os
from datetime import datetime
from collections import defaultdict

class Transaction:
    def __init__(self, trans_type, amount, category, description, date=None):
        self.trans_type = trans_type
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "type": self.trans_type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

    def __str__(self):
        return f"{self.date} | {self.trans_type} | ₹{self.amount:.2f} | {self.category} | {self.description}"

class FinanceTracker:
    def __init__(self, filename="transactions.json"):
        self.filename = filename
        self.transactions = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        self.transactions.append(Transaction(
                            item["type"], item["amount"], item["category"], 
                            item["description"], item.get("date")
                        ))
            except:
                pass
        else:
            self.transactions = [
                Transaction("Income", 5000, "Salary", "Monthly salary"),
                Transaction("Expense", 1200, "Food", "Groceries"),
                Transaction("Expense", 800, "Transport", "Cab fare")
            ]
            self.save_data()

    def save_data(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump([t.to_dict() for t in self.transactions], f, indent=4)
        except:
            pass

    def view_transactions(self):
        print("\n--- Transaction History ---")
        print("Date         Type       Amount       Category       Description")
        print("-" * 75)
        for t in self.transactions:
            print(f"{t.date:<12} {t.trans_type:<10} ₹{t.amount:<10.2f} {t.category:<14} {t.description}")

    def calculate_balance(self):
        balance = sum(t.amount if t.trans_type == "Income" else -t.amount for t in self.transactions)
        return balance

    def monthly_report(self):
        monthly = defaultdict(float)
        for t in self.transactions:
            if t.trans_type == "Expense":
                month = t.date[:7]
                monthly[month] += t.amount
        print("\n--- Monthly Expense Report ---")
        for m in sorted(monthly):
            print(f"{m}: ₹{monthly[m]:.2f}")

    def demo(self):
        print("=== FinanceFlow Demo ===")
        self.view_transactions()
        print(f"\nTotal Balance: ₹{self.calculate_balance():.2f}")
        self.monthly_report()
        print("\nDemo complete. For full interactive version use local Python.")

print("Starting FinanceFlow Demo...")
tracker = FinanceTracker()
tracker.demo()