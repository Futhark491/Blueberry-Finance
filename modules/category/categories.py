import re
import modules.standard.stdfn as stdfn
from flask import flash


# Validates all data from categories.
# Returns False if the data validation failed and True otherwise
def validate_category_data(name, amount):
    moneyStringRegex = "[0-9]+(\.[0-9][0-9])?"

    succeeded = True

    if not stdfn.verify_input_sanitization(name):
        flash('Invalid category name. Please resubmit.')
        succeeded = False
    if not (stdfn.verify_input_sanitization(amount) and
            re.fullmatch(moneyStringRegex, amount)):
        flash("Invalid amount. Please resubmit.")
        succeeded = False

    return succeeded
