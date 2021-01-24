import sqlite3
from flask import Flask
from flask import render_template, request, redirect
from helpers import format_amount_view_expense


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Home Page, placeholder
@app.route('/')
def index():
    return render_template('index.html', title='Index')

# Create List Expenses site
@app.route('/list')
def list_expense():
    query = "SELECT ExpenseDate, ExpenseDescription, CategoryName, ACCOUNTS.AccountName, ExpenseAmount, ExpenseId FROM EXPENSES JOIN ACCOUNTS ON EXPENSES.AccountId=ACCOUNTS.AccountId JOIN CATEGORIES ON EXPENSES.CategoryId=CATEGORIES.CategoryId ORDER BY ExpenseDate"
    with sqlite3.connect("main.db") as connection:
        cursor = connection.cursor()
        table_list_data = cursor.execute(query)
    return render_template('expense_list.html', title='Expenses', table_list_data=table_list_data)

# Create View Single Expenses site,
# as per https://pythonise.com/series/learning-flask/generating-dynamic-urls-with-flask
@app.route("/view/<expense_id>")
def profile(expense_id):
    query = f"SELECT ExpenseDate, ExpenseDescription, CategoryName, ACCOUNTS.AccountName, ExpenseAmount, ExpenseId FROM EXPENSES JOIN ACCOUNTS ON EXPENSES.AccountId=ACCOUNTS.AccountId JOIN CATEGORIES ON EXPENSES.CategoryId=CATEGORIES.CategoryId WHERE ExpenseId={expense_id}"
    with sqlite3.connect("main.db") as connection:
        cursor = connection.cursor()
        table_list_data = cursor.execute(query)
        for data in table_list_data:
            expense_data = [data[0], data[1], data[2], data[3], format_amount_view_expense(data[4])]
            break
        # Falta crear una funcion que traiga los tres gastos mas relevantes para mostrar debajo del gasto principal...
    return render_template("expense_view.html", expense_data=expense_data)
