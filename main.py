import os
from flask import Flask, render_template, request, session, redirect, flash
import modules.user_acct.user_acct as user_acct
import modules.db.DbFunctions as DbFunctions
import modules.transactions.transactions as ta
import modules.standard.stdfn as stdfn


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

        # Get default categories from the user and add them to the transaction
        # selection list for adding transactions
        category_list = DbFunctions.get_categories(username,
                                                   user_table,
                                                   category_table)
        transaction_list = DbFunctions.get_transactions(username,
                                                        user_table,
                                                        transaction_table)

        return render_template('main.html',
                               username=username,
                               category_list=category_list,
                               transaction_list=transaction_list)


# Adds a transaction to the database
@app.route('/add_transaction', methods=['POST'])
def add_transaction_action():
    username = session.get('user_data').get('username')
    description = request.form['transaction_description']
    amount = request.form['transaction_amount']
    date = request.form['transaction_date']
    category = request.form['transaction_category']

    # Sanitize inputs
    if ta.validate_transaction_data(description, amount, date, category):
        # Add transaction to database
        DbFunctions.add_trans(username, user_table,
                              category, amount,
                              description, date,
                              transaction_table)

    return redirect('/')


# Removes the transaction with a given ID
# (note that this uses the URL query '?id=XXX')
@app.route('/remove_transaction')
def remove_transaction_action():
    transaction_id = int(request.args.get('id'))
    username = session.get('user_data').get('username')
    # Verify that the user owns the transaction and remove it
    transaction_list = DbFunctions.get_transactions(username,
                                                    user_table,
                                                    transaction_table)
    for transaction_data in transaction_list:
        if transaction_data[0] == transaction_id:
            DbFunctions.remove_trans(transaction_id, transaction_table)
            flash('Your transaction was removed.')
            return redirect('/')

    # Transaction not found/ not owned by the user
    flash('There was an error removing the transaction.')

    return redirect('/')


# Redirects the user to a form page to edit the transaction data,
# or back to the dashboard if no transactions were found
@app.route('/edit_transaction')
def edit_transaction_page():
    username = session.get('user_data').get('username')
    transaction_id = int(request.args.get('id'))

    # Get the transaction from the database if the user owns it
    # (code below is temporary, using the description as the ID)
    transaction_list = DbFunctions.get_transactions(username,
                                                    user_table,
                                                    transaction_table)
    for transaction_data in transaction_list:
        if transaction_data[0] == transaction_id:
            category_list = DbFunctions.get_categories(username,
                                                       user_table,
                                                       category_table)
            return render_template('transactionEditor.html',
                                   username=username,
                                   category_list=category_list,
                                   transaction_data=transaction_data)

    # Transaction not found/ not owned by the user
    flash('There was an error editing the transaction.')
    return redirect('/')


# Saves the edits to the server and redirects the user back to the dashboard
@app.route('/commit_transaction_edits', methods=['POST'])
def edit_transaction_action():
    db_id = int(request.args.get('id'))
    description = request.form['transaction_description']
    amount = request.form['transaction_amount']
    date = request.form['transaction_date']
    category = request.form['transaction_category']

    succeed = False

    # Sanitize inputs
    if ta.validate_transaction_data(description, amount, date, category):
        db_commit_success = DbFunctions.edit_trans(db_id, category,
                                                   amount, description,
                                                   date, transaction_table)
        if db_commit_success:
            succeed = True
            flash('Your transaction has been updated.')

    if not succeed:
        flash('Your transaction could not be updated.')

    return redirect('/')


# Adds a category to the database
@app.route('/add_category', methods=['POST'])
def add_category_action():
    username = session.get('user_data').get('username')
    name = request.form['category_name']
    value = request.form['transaction_amount']

    # Sanitize inputs
    if not stdfn.verify_input_sanitization(name):
        flash('Invalid category name.')
        return redirect('/')
    if not stdfn.verify_input_sanitization(value):
        flash('Invalid category value.')
        return redirect('/')

    # Add transaction to database
    if (DbFunctions.add_cat(username, user_table,
                            name, value, category_table)):
        flash('Category added.')
    else:
        flash('Failed to add category.')

    return redirect('/')


# Removes the transaction with a given ID
# (note that this uses the URL query '?id=XXX')
@app.route('/remove_category')
def remove_category_action():
    category_id = int(request.args.get('id'))
    username = session.get('user_data').get('username')
    # Verify that the user owns the transaction and remove it
    category_list = DbFunctions.get_categories(username,
                                               user_table,
                                               transaction_table)
    for category_data in category_list:
        if (category_data[0] == category_id and category_data[1] is not 'Uncategorized'):

            DbFunctions.remove_cat(category_id, category_table)
            flash('Your category was removed.')
            return redirect('/')

    # Transaction not found/ not owned by the user
    flash('There was an error removing the category.')

    return redirect('/')


# Processes login data
@app.route('/login', methods=['POST'])
def login_action():
    session['logged_in'] = user_acct.validate_login_data(
        request.form['username'],
        request.form['password'],
        user_table)

    # Set up the user data as needed
    if session['logged_in']:
        session['user_data'] = {'username': request.form['username']}

    return redirect('/')


# Forces users back to login screen & deletes stored session data
@app.route('/logout')
def logout_action():
    session['logged_in'] = False

    session['user_data'] = None

    return redirect('/')


# Send users to the registration page to make an account
@app.route('/registration')
def registration_page():
    return render_template('register.html')


# Pull data from the registration form and attempt to create a new user.
# Redirect to home (for logging in) if it succeeds.
@app.route('/register', methods=['POST'])
def register_action():

    # Pull data from the form, sanitize it, and add it to the DB
    successful_registration = user_acct.validate_registration_data(
        request.form['username'],
        request.form['password'],
        user_table, category_table,
        DEFAULT_USER_CATEGORIES)

    if successful_registration:
        return redirect('/')
    else:
        return redirect('/registration')


# Run the flask application
if __name__ == "__main__":
    # debug code for cookies
    app.secret_key = os.urandom(12)
    # run the application
    app.run(debug=True, host=APP_HOST, port=APP_PORT)
