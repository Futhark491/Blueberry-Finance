import os
import json
import datetime
from flask import Flask, render_template, request, session, redirect, flash
import modules.user_acct.user_acct as user_acct
import modules.db.DbFunctions as DbFunctions
import modules.transactions.transactions as ta
import modules.category.categories as cat
import modules.standard.stdfn as stdfn


# Static variables
APP_HOST = '127.0.0.1'
APP_PORT = 5000
DEFAULT_USER_CATEGORIES = {'Food': '25',
                           'Car': '50',
                           'Personal': '25'}
DEFAULT_USER_INCOME = 0

# build the flask application
app = Flask(__name__)

# load up the database tables
master = DbFunctions.load_db()


# Main page
@app.route('/')
def home_page():
    budget_pie_chart_data = {'cols': [{'label': 'Category',
                                       'type': 'string'},
                                      {'label': 'Amount',
                                       'type': 'number'}],
                             'rows': []}

    transaction_pie_chart_data = {'cols': [{'label': 'Category',
                                            'type': 'string'},
                                           {'label': 'Amount',
                                            'type': 'number'}],
                                  'rows': []}
    # Validate user log in
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        username = session.get('user_data').get('username')

        view_month = request.args.get('month')
        view_year = request.args.get('year')

        if(view_month is None):
            view_month = str(datetime.datetime.today().month).zfill(2)
        if(view_year is None):
            view_year = str(datetime.datetime.today().year).zfill(4)

        # Get default categories from the user and add them to the transaction
        # selection list for adding transactions
        category_list = DbFunctions.get_categories(username,
                                                   master)
        transaction_list = DbFunctions.get_transactions(username,
                                                        view_month,
                                                        view_year,
                                                        master)

        # Create a dictionary for each category that stores the spending for
        # that category. The key is the category ID and the value is the sum
        # of all transaction values related to that category.
        transaction_sum = {}
        for category in category_list:
            transaction_sum[category[0]] = 0

        # Convert the number to have a cents place regardless of value after
        # adding the value to the sum total for the related category.
        for transaction in transaction_list:
            transaction_sum[int(transaction[1])] += transaction[2]
            # Convert number to string and add decimals where necessary
            transaction[2] = stdfn.add_cents(str(transaction[2]))

        # Convert number to string and add decimals where necessary. Then add
        # in the transaction where needed
        for category in category_list:
            # Add the data to the chart
            budget_pie_chart_data['rows'].append({'c': [{'v': category[1]},
                                                        {'v': category[2]}]})
            transaction_pie_chart_data['rows'].append({'c':[{'v':category[1]},
                                                            {'v':transaction_sum[category[0]]}]})
            # Format the numbers in the table
            category[2] = stdfn.add_cents(str(category[2]))
            # Format and add the actual spending to the table
            category.append(stdfn.add_cents(str(transaction_sum[category[0]])))

            income_formatted = stdfn.add_cents(str(DbFunctions.get_income(username, master)))

        return render_template('main.html',
                               username=username,
                               income=income_formatted,
                               category_list=category_list,
                               transaction_list=transaction_list,
                               budget_chart_json=json.dumps(budget_pie_chart_data),
                               transaction_chart_json=json.dumps(transaction_pie_chart_data))


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
        DbFunctions.add_trans(username, category, amount,
                              description, date,
                              master)

    return redirect('/')


# Removes the transaction with a given ID
# (note that this uses the URL query '?id=XXX')
@app.route('/remove_transaction')
def remove_transaction_action():
    transaction_id = int(request.args.get('id'))
    username = session.get('user_data').get('username')
    
    view_month = request.args.get('month')
    view_year = request.args.get('year')

    if(view_month is None):
      view_month = str(datetime.datetime.today().month).zfill(2)
    if(view_year is None):
      view_year = str(datetime.datetime.today().year).zfill(4)

    # Verify that the user owns the transaction and remove it
    transaction_list = DbFunctions.get_transactions(username,
                                                    view_month,
                                                    view_year,
                                                    master)
    for transaction_data in transaction_list:
        if transaction_data[0] == transaction_id:
            DbFunctions.remove_trans(transaction_id, master)
            flash('Your transaction was removed.')
            return redirect('/')

    # Transaction not found/ not owned by the user
    flash('There was an error removing the transaction.')

    return redirect('/')


# Saves the transaction edits to the server
# and redirects the user back to the dashboard
@app.route('/edit_transaction', methods=['POST'])
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
                                                   date, master)
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
    value = request.form['category_value']

    # Sanitize inputs
    if cat.validate_category_data(name, value):
        # Add transaction to database
        if (DbFunctions.add_cat(username,
                                name, value, master)):
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
                                               master)
    for category_data in category_list:
        if (category_data[0] == category_id and
                category_data[1] is not 'Uncategorized'):

            DbFunctions.remove_cat(category_id,
                                   master)
            flash('Your category was removed.')
            return redirect('/')

    # Transaction not found/ not owned by the user
    flash('There was an error removing the category.')

    return redirect('/')


# Saves the category edits to the server
# and redirects the user back to the dashboard
@app.route('/edit_category', methods=['POST'])
def edit_category_action():
    db_id = int(request.args.get('id'))
    name = request.form['category_name']
    value = request.form['category_value']

    # Sanitize inputs
    if cat.validate_category_data(name, value):
        # Add transaction to database
        if DbFunctions.edit_cat(db_id, name, value, master):
            flash('Category changed.')
        else:
            flash('Failed to add category.')

    return redirect('/')


# Processes login data
@app.route('/login', methods=['POST'])
def login_action():
    session['logged_in'] = user_acct.validate_login_data(
        request.form['username'],
        request.form['password'],
        master)

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
        DEFAULT_USER_INCOME,
        DEFAULT_USER_CATEGORIES,
        master)

    if successful_registration:
        return redirect('/')
    else:
        return redirect('/registration')


@app.route('/change_income', methods=['POST'])
def change_income_action():
    username = session.get('user_data').get('username')

    user_acct.validate_income(username, request.form['income'], master)

    return redirect('/')


# Run the flask application
if __name__ == "__main__":
    # debug code for cookies
    app.secret_key = os.urandom(12)
    # run the application
    app.run(debug=True, host=APP_HOST, port=APP_PORT)
