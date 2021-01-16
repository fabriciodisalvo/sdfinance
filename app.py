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