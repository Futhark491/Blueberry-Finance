from flask import flash
import stdfn

# Verify that the username & password are sanitary and is a valid
# combination saved in the database
def validate_login_data(username,password):
    # Sanitize inputs
    # (note that this does NOT validate the usr/pwd combo)
    if not stdfn.verify_input_sanitization(username,username):
        flash('Username is invalid')
        return False
    if not stdfn.verify_input_sanitization(password):
        flash('Password is invalid')
        return False

    # TODO: check username and password combo against DB
    #       If this check fails, flash an auth fail
    if not db_user_check_example(username.lower(),password):
        flash('Could not find your account.')
        return False

    return True

# TEMPORARY proof-of-concept method that "checks" for a valid database
# entry (uname = admin, pwd = admin)
def db_user_check_example(username,password):
    return (username == 'admin' and password == 'admin')
