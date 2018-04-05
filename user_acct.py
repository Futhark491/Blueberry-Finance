from flask import flash
import modules.standard.stdfn as stdfn
import modules.db.DbFunctions as DbFunctions


# Verify that the username & password are sanitary and is a valid
# combination saved in the database
def validate_login_data(username, password, user_table):
    succeeded = True

    # Sanitize inputs
    # (note that this does NOT validate the usr/pwd combo)
    if not stdfn.verify_input_sanitization(username):
        flash('Username is invalid')
        succeeded = False
    if not stdfn.verify_input_sanitization(password):
        flash('Password is invalid')
        succeeded = False

    # Check username and password combo against DB
    if succeeded and not DbFunctions.validate_user(username.lower(), password, user_table):
        flash('Could not find your account.')
        succeeded = False

    return succeeded


def validate_registration_data(username, password, user_table, category_table, default_categories):
    succeeded = True

    # Sanitize inputs
    if not stdfn.verify_input_sanitization(username.lower(), 'username'):
        flash('Username must have between 5-15 characters')
        succeeded = False
    if not stdfn.verify_input_sanitization(password, 'password'):
        flash('Password must not be empty')
        succeeded = False
        
    # Add username and password to the database
    if succeeded and not DbFunctions.add_user(username.lower(), password, user_table, category_table, default_categories):
        flash('Username is already in the database.')
        succeeded = False

    if succeeded:
        flash('Your account was created successfully.')
    
    return succeeded
