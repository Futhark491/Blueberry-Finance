import os
from flask import Flask, flash, render_template, request, session, redirect
import user_acct

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

    session['logged_in'] = user_acct.validate_login_data(request.form['username'],request.form['password'])

    return redirect('/')

# Forces users back to login screen
@app.route('/logout')
def logout():
    session['logged_in'] = False

    return redirect('/')

# Run the flask application
if __name__ == "__main__":
    #debug code for cookies
    app.secret_key = os.urandom(12)
    # run the application
    app.run(debug=True, host=APP_HOST, port=APP_PORT)
