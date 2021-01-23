import sqlite3
from flask import Flask
from flask import render_template, request, redirect


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def index():
    return render_template('index.html', title='Index')

@app.route('/list')
def list_expense():
    query = "SELECT ExpenseDate, ExpenseDescription, CategoryName, ACCOUNTS.AccountName, ExpenseAmount FROM EXPENSES JOIN ACCOUNTS ON EXPENSES.AccountId=ACCOUNTS.AccountId JOIN CATEGORIES ON EXPENSES.CategoryId=CATEGORIES.CategoryId ORDER BY ExpenseDate"
    with sqlite3.connect("main.db") as connection:
        cursor = connection.cursor()
        table_list_data = cursor.execute(query)
    return render_template('expense_list.html', title='Expenses', table_list_data=table_list_data)

@app.route('/new')
def add_expense():
    return render_template('expense_add.html', title='Add Expense')