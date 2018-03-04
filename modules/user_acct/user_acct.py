from flask import flash
import modules.standard.stdfn as stdfn
import modules.db.DbFunctions as DbFunctions


# Verify that the username & password are sanitary and is a valid
# combination saved in the database
def validate_login_data(username, password, user_table):
    # Sanitize inputs
    # (note that this does NOT validate the usr/pwd combo)
    if not stdfn.verify_input_sanitization(username):
        flash('Username is invalid')
        return False
    if not stdfn.verify_input_sanitization(password):
        flash('Password is invalid')
        return False

    # Check username and password combo against DB
    if not DbFunctions.validate_user(username.lower(), password, user_table):
        flash('Could not find your account.')
        return False

    return True


def validate_registration_data(username, password, user_table, category_table, default_categories):
    # Sanitize inputs
    if not stdfn.verify_input_sanitization(username.lower(), 'username'):
        flash('Username must have between 5-15 characters')
        return False
    if not stdfn.verify_input_sanitization(password, 'password'):
        flash('Password must not be empty')
        return False

    # TODO: Check to see if user is in DB already

    # Add username and password to the database
    DbFunctions.add_user(username.lower(), password, user_table, category_table, default_categories)

    flash('Your account was created successfully.')
    return True
