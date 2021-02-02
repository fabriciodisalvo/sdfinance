import sqlite3
from flask import Flask
from flask import render_template, request, redirect, flash
from helpers import format_amount_view_expense


# Set up database
connection = sqlite3.connect("main.db", check_same_thread=False)
cursor = connection.cursor()

# Configure application
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Home Page, placeholder
@app.route('/')
def index():
    return render_template('index.html', title='Index')

# Create List Expenses site
@app.route('/list')
def list_expense():
    query = "SELECT ExpenseDate, ExpenseDescription, CategoryName, ACCOUNTS.AccountName, ExpenseAmount, ExpenseStatus, ExpenseId FROM EXPENSES JOIN ACCOUNTS ON EXPENSES.AccountId=ACCOUNTS.AccountId JOIN CATEGORIES ON EXPENSES.CategoryId=CATEGORIES.CategoryId  WHERE ExpenseStatus<>'Deleted' ORDER BY ExpenseDate"
    table_list_data = cursor.execute(query)
    return render_template('expense_list.html', title='Expenses', table_list_data=table_list_data)

# Create View Single Expenses site,
# as per https://pythonise.com/series/learning-flask/generating-dynamic-urls-with-flask
@app.route("/view/<expense_id>")
def view(expense_id):
    query = f"SELECT ExpenseDate, ExpenseDescription, CategoryName, ACCOUNTS.AccountName, ExpenseAmount, ExpenseId FROM EXPENSES JOIN ACCOUNTS ON EXPENSES.AccountId=ACCOUNTS.AccountId JOIN CATEGORIES ON EXPENSES.CategoryId=CATEGORIES.CategoryId WHERE ExpenseId={expense_id}"
    table_list_data = cursor.execute(query)
    for data in table_list_data:
        expense_data = [data[0], data[1], data[2], data[3], format_amount_view_expense(data[4]), data[5]]
        break
        # Falta crear una funcion que traiga los tres gastos mas relevantes para mostrar debajo del gasto principal...
    return render_template("expense_view.html", expense_data=expense_data)

# Create Delete Single Expenses site
@app.route("/delete/<expense_id>")
def delete(expense_id):
    query = f"SELECT ExpenseDate, ExpenseDescription, CategoryName, ACCOUNTS.AccountName, ExpenseAmount, ExpenseId FROM EXPENSES JOIN ACCOUNTS ON EXPENSES.AccountId=ACCOUNTS.AccountId JOIN CATEGORIES ON EXPENSES.CategoryId=CATEGORIES.CategoryId WHERE ExpenseId={expense_id}"
    table_list_data = cursor.execute(query)
    for data in table_list_data:
        expense_data = [data[0], data[1], data[2], data[3], format_amount_view_expense(data[4]), data[5]]
        break
    return render_template("expense_delete.html", expense_data=expense_data)

# Create Deleted Expenses placeholder
@app.route("/deleted/<expense_id>")
def deleted(expense_id):
    query = f"UPDATE EXPENSES SET ExpenseStatus= 'Deleted' WHERE ExpenseId={expense_id};"
    table_list_data = cursor.execute(query)
    connection.commit()
    return render_template("expense_deleted.html")

# Create Add Single Expense site
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        categories_data = list(cursor.execute("SELECT CategoryId, CategoryName FROM CATEGORIES"))
        accounts_data = list(cursor.execute("SELECT AccountId, AccountName FROM ACCOUNTS"))
        return render_template("expense_add.html", categories_data=categories_data, accounts_data=accounts_data)
    else:
        description = request.form.get("description")
        amount = float(request.form.get("amount")) * -1
        category = request.form.get("category")
        account = request.form.get("account")
        date = '2020.01.25'
        query = f"INSERT INTO EXPENSES (ExpenseDate, ExpenseDescription, CategoryId, AccountId, ExpenseAmount) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (date, description, category, account, amount))
        connection.commit()
        flash('Expense added')
        return redirect("/list")