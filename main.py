
import csv
import os
from datetime import datetime

# CSV file name
FILE_NAME = "expenses.csv"

# CSV column headings
HEADERS = ["Date", "Category", "Description", "Amount"]


# ==========================================
# INITIALIZE CSV FILE
# ==========================================

def initialize_file():

    if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:

        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)
            writer.writerow(HEADERS)


# ==========================================
# ADD EXPENSE
# ==========================================

def add_expense():

    print("\n===== ADD NEW EXPENSE =====")

    # Get date
    while True:

        date_input = input(
            "Enter date (YYYY-MM-DD) or press Enter for today: "
        ).strip()

        if date_input == "":
            expense_date = datetime.now().strftime("%Y-%m-%d")
            break

        try:
            expense_date = datetime.strptime(
                date_input, "%Y-%m-%d"
            ).strftime("%Y-%m-%d")
            break

        except ValueError:
            print("Invalid date! Use YYYY-MM-DD format.")

    # Get category
    categories = [
        "Food",
        "Travel",
        "Shopping",
        "Education",
        "Bills",
        "Healthcare",
        "Other"
    ]

    print("\nAvailable Categories:")

    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    while True:

        choice = input("Select category (1-7): ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = categories[int(choice) - 1]
            break

        print("Invalid category! Please select between 1 and 7.")

    # Get description
    while True:

        description = input("Enter expense description: ").strip()

        if description:
            break

        print("Description cannot be empty.")

    # Get amount
    while True:

        try:

            amount = float(input("Enter amount (₹): "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            break

        except ValueError:
            print("Invalid amount! Enter a numeric value.")

    # Save expense in CSV
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            expense_date,
            category,
            description,
            f"{amount:.2f}"
        ])

    print("\nExpense added successfully!")


# ==========================================
# READ ALL EXPENSES
# ==========================================

def read_expenses():

    initialize_file()

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        expenses = list(reader)

    return expenses


# ==========================================
# VIEW ALL EXPENSES
# ==========================================

def view_expenses():

    print("\n===== ALL EXPENSES =====")

    expenses = read_expenses()

    if not expenses:

        print("No expenses recorded yet.")
        return

    total = 0

    print("-" * 75)

    print(
        f"{'Date':<13} {'Category':<13} "
        f"{'Description':<25} {'Amount':>12}"
    )

    print("-" * 75)

    for expense in expenses:

        amount = float(expense["Amount"])

        total += amount

        print(
            f"{expense['Date']:<13} "
            f"{expense['Category']:<13} "
            f"{expense['Description'][:24]:<25} "
            f"₹{amount:>10.2f}"
        )

    print("-" * 75)

    print(f"Total Expenses: ₹{total:.2f}")


# ==========================================
# FILTER EXPENSES BY CATEGORY
# ==========================================

def filter_expenses():

    print("\n===== FILTER EXPENSES =====")

    expenses = read_expenses()

    if not expenses:
        print("No expenses available to filter.")
        return

    category = input(
        "Enter category to filter (e.g. Food, Travel): "
    ).strip()

    if not category:
        print("Category cannot be empty.")
        return

    filtered = [
        expense for expense in expenses
        if expense["Category"].lower() == category.lower()
    ]

    if not filtered:

        print("No expenses found in this category.")
        return

    total = 0

    print(f"\nExpenses in category: {category}")

    for expense in filtered:

        amount = float(expense["Amount"])

        total += amount

        print(
            f"{expense['Date']} | "
            f"{expense['Description']} | "
            f"₹{amount:.2f}"
        )

    print(f"\nCategory Total: ₹{total:.2f}")


# ==========================================
# CATEGORY SUMMARY
# ==========================================

def category_summary():

    print("\n===== CATEGORY-WISE SUMMARY =====")

    expenses = read_expenses()

    if not expenses:
        print("No expenses recorded yet.")
        return

    summary = {}

    for expense in expenses:

        category = expense["Category"]

        amount = float(expense["Amount"])

        if category not in summary:
            summary[category] = 0

        summary[category] += amount

    grand_total = sum(summary.values())

    for category, total in summary.items():

        percentage = (total / grand_total) * 100

        print(
            f"{category:<15} "
            f"₹{total:>10.2f} "
            f"({percentage:.1f}%)"
        )

    print("-" * 40)

    print(f"{'Grand Total':<15} ₹{grand_total:.2f}")


# ==========================================
# MAIN MENU
# ==========================================

def main():

    initialize_file()

    while True:

        print("\n====================================")
        print("       PERSONAL EXPENSE TRACKER")
        print("====================================")

        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter Expenses by Category")
        print("4. Category-wise Summary")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":

            add_expense()

        elif choice == "2":

            view_expenses()

        elif choice == "3":

            filter_expenses()

        elif choice == "4":

            category_summary()

        elif choice == "5":

            print("\nThank you for using Personal Expense Tracker!")
            print("Goodbye!")
            break

        else:

            print("Invalid choice! Please select between 1 and 5.")


# Run application
if __name__ == "__main__":

    main()
