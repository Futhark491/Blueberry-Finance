import os
from flask import Flask, render_template, request, session, redirect, flash
import modules.user_acct.user_acct as user_acct
import modules.db.DbFunctions as DbFunctions
import re


# Static variables
APP_HOST = '127.0.0.1'
APP_PORT = 5000
DEFAULT_USER_CATEGORIES = {'Food': 25, 'Car': 50, 'Personal': 25}

# build the flask application
app = Flask(__name__)

# load up the database tables
user_table = DbFunctions.load_user()
category_table = DbFunctions.load_cat()
transaction_table = DbFunctions.load_tran()


# Main page
@app.route('/')
def home_page():
    # Validate user log in
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        username = session.get('user_data').get('username')

        # Get default categories from the user and add them to the transaction selection list for adding transactions
        category_dict = DbFunctions.get_catagories(username, user_table, category_table)
        transaction_list = DbFunctions.get_transactions(username, user_table, transaction_table)

        return render_template('main.html', username=username, category_dict=category_dict, transaction_list=transaction_list)


# Adds a transaction to the database
@app.route('/add_transaction', methods=['POST'])
def add_transaction_action():
    username = session.get('user_data').get('username')
    description = request.form['transaction_description']
    amount = request.form['transaction_amount']
    date = request.form['transaction_date']
    category = request.form['transaction_category']

    print("\n\n" + category + "\n\n")

    # Sanitize inputs
    if validate_transaction_data(description, amount, date, category):
        # Add transaction to database
        DbFunctions.add_trans(username, user_table, category, amount, description, date, transaction_table)

    return redirect('/')


# Removes the transaction with a given ID (note that this uses the URL query '?id=XXX')
@app.route('/remove_transaction')
def remove_transaction_action():
    username = session.get('user_data').get('username')
    transaction_id = request.args.get('id')

    # TODO: verify that the user owns the transaction and remove it
    print("\n\nTransaction to remove: {0}".format(transaction_id))

    return redirect('/')


# Processes login data
@app.route('/login', methods=['POST'])
def login_action():
    session['logged_in'] = user_acct.validate_login_data(request.form['username'], request.form['password'], user_table)

    # Set up the user data as needed
    if session['logged_in']:
        session['user_data'] = {'username': request.form['username']}

    return redirect('/')


# Forces users back to login screen & deletes stored data
@app.route('/logout')
def logout_action():
    session['logged_in'] = False

    session['user_data'] = None

    return redirect('/')


# Send users to the registration page to make an account
@app.route('/registration')
def registration_page():
    return render_template('register.html')


# Pull data from the registration form and attempt to create a new user. Redirect to home (for logging in) if it succeeds.
@app.route('/register', methods=['POST'])
def register_action():

    # Pull data from the form, sanitize it, and add it to the DB
    successful_registration = user_acct.validate_registration_data(request.form['username'], request.form['password'], user_table, category_table, DEFAULT_USER_CATEGORIES)

    if successful_registration:
        return redirect('/')
    else:
        return redirect('/registration')


# Validates all data from transactions. Returns False if the data validation failed and True otherwise
def validate_transaction_data(description, amount, date, category):
    moneyStringRegex = "-?[0-9]+(\.[0-9][0-9])?"
    dateStringRegex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]"

    if description == '' or amount == '' or date == '' or category == '':
        flash('Fields cannot be left blank')
        return False
    elif not re.fullmatch(moneyStringRegex, amount):
        flash("Invalid Amount. Please resubmit.")
        return False
    elif not re.fullmatch(dateStringRegex, date):
        flash("Invalid Date. Please resubmit.")
        return False

    return True


# Run the flask application
if __name__ == "__main__":
    # debug code for cookies
    app.secret_key = os.urandom(12)
    # run the application
    app.run(debug=True, host=APP_HOST, port=APP_PORT)
