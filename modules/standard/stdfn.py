

# Standard sanitation of a given input. If the input is not valid in any
# way, return False. Otherwise, return True.
# An optional input type value can be inserted as well, to get more
# specific sanitization checks, including 'username' and 'password'.
def verify_input_sanitization(input_string, input_type='none'):
    # GENERIC SANITATION
    # Nonetype
    if input_string is None:
        return False
    # Empty string
    elif input_string == '':
        return False

    # username sanitization
    elif input_type == 'username':
        # username too short / long
        if len(input_string) < 4 or len(input_string) > 16:
            return False
        elif input_string == 'master':
            return False
    elif input_type == 'password':
        pass

    # Input is sanitary
    return True


def add_cents(dollar_value_string):
    # If there is a decimal place already in the number
    if '.' in dollar_value_string:
        # If there is only one number after the decimal
        if dollar_value_string[-2] == '.':
            # Add a zero to the end
            dollar_value_string += '0'
    # If there isn't a decimal in the number already
    else:
        # Add placeholders
        dollar_value_string += '.00'

    # return the modified value
    return dollar_value_string
