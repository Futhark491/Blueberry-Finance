from flask import flash
import modules.standard.stdfn as stdfn
import modules.db.DbFunctions as DbFunctions

# Verify that the username & password are sanitary and is a valid
# combination saved in the database
def validate_login_data(username,password,user_table):
    # Sanitize inputs
    # (note that this does NOT validate the usr/pwd combo)
    if not stdfn.verify_input_sanitization(username,'username'):
        flash('Username is invalid')
        return False
    if not stdfn.verify_input_sanitization(password):
        flash('Password is invalid')
        return False

    # TODO: check username and password combo against DB
    #       If this check fails, flash an auth fail
    if not DbFunctions.validate_user(username.lower(),password,user_table):
        flash('Could not find your account.')
        return False

    return True
