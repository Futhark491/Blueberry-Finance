import os
from flask import Flask, flash, render_template, request, session, redirect
import stdfn

# Static variables
APP_HOST = '127.0.0.1'
APP_PORT = 5000

# build the flask application
app = Flask(__name__)

# Main page
@app.route('/')
def home():
    # Validate user log in
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return '<h1>You are logged in.</h1><a href="/logout">Log out.</a>'

# Processes login data
@app.route('/login', methods=['POST'])
def login():
    # Get username/password from form
    form_username = str(request.form['username']).lower()
    form_password = str(request.form['password'])

    # Flag to verify that logging in didn't fail at any point.
    success = True

    # Sanitize inputs (note that this does NOT validate the usr/pwd combo)
    if not stdfn.sanitize_input(form_username):
        success = False
        flash('Username is invalid')
    if not stdfn.sanitize_input(form_password):
        success = False
        flash('Password is invalid')

    # Query database for validity
    if success:
        # TODO: check username and password against DB
        #       If this check fails, flash an auth fail & change success
        pass
    else:
        # Input wasn't sanitary, so just redirect back to home without validating.
        return redirect('/')

    # Create a data container to store session data
    if success:
        session['logged_in'] = True
    else:
        flash('Incorrect username or password.')

    return redirect('/')

# Forces users back to login screen
@app.route('/logout')
def logout():
    session['logged_in'] = False

    return redirect('/')

# Run the flask application
if __name__ == "__main__":
    #debug code
    app.secret_key = os.urandom(12)
    # run the application
    app.run(debug=True, host=APP_HOST, port=APP_PORT)