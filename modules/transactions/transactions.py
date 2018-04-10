import re
import modules.standard.stdfn as stdfn
from flask import flash


# Validates all data from transactions.
# Returns False if the data validation failed and True otherwise
def validate_transaction_data(description, amount, date, category):
    moneyStringRegex = "[0-9]+(\.[0-9][0-9])?"
    dateStringRegex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]"

    succeeded = True

    if not stdfn.verify_input_sanitization(description):
        flash('Invalid description. Please resubmit.')
        succeeded = False
    if not (stdfn.verify_input_sanitization(amount) and
            re.fullmatch(moneyStringRegex, amount)):
        flash("Invalid amount. Please resubmit.")
        succeeded = False
    if not (stdfn.verify_input_sanitization(date) and
            re.fullmatch(dateStringRegex, date)):
        flash("Invalid date. Please resubmit.")
        succeeded = False
    if not stdfn.verify_input_sanitization(category):
        flash('Invalid category. Please resubmit.')
        succeeded = False

    return succeeded
