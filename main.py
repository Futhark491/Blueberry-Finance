import os
from flask import Flask, render_template, request, session, redirect
import modules.user_acct.user_acct as user_acct
import modules.db.DbFunctions as DbFunctions

# Static variables
APP_HOST = '127.0.0.1'
APP_PORT = 5000
DEFAULT_USER_CATEGORIES = []

# build the flask application
app = Flask(__name__)

# load up the usertable
user_table = DbFunctions.load_user()
category_table = DbFunctions.load_cat()


# Main page
@app.route('/')
def home():
    # Validate user log in
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        #redirect('/main')
        return render_template('main.html', username=session.get('user_data').get('username'))


@app.route('/main', methods=['POST'])
def main():
    description = request.form['transaction_description']
    price = request.form['transaction_price']

    #TODO add transaction details to database associated with current user
    return render_template('main.html', username=session.get('user_data').get('username'))

# Processes login data
@app.route('/login', methods=['POST'])
def login():
    session['logged_in'] = user_acct.validate_login_data(request.form['username'], request.form['password'], user_table)

    # Set up the user data as needed
    if session['logged_in']:
        session['user_data'] = {'username': request.form['username']}

    return redirect('/')


# Forces users back to login screen & deletes stored data
@app.route('/logout')
def logout():
    session['logged_in'] = False

    session['user_data'] = None

    return redirect('/')


# Send users to the registration page to make an account
@app.route('/registration')
def registration():
    return render_template('register.html')


# Pull data from the registration form and attempt to create a new user. Redirect to home (for logging in) if it succeeds.
@app.route('/register', methods=['POST'])
def register_action():

    # TODO: Pull data from the form, sanitize it, and add it to the DB
    successful_registration = user_acct.validate_registration_data(request.form['username'], request.form['password'], user_table, category_table, DEFAULT_USER_CATEGORIES)

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
