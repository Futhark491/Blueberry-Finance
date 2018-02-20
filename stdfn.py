# Standard sanitation of a given input. If the input is not valid in any
# way, return False. Otherwise, return True.
# An optional input type value can be inserted as well, to get more
# specific sanitization checks, including 'username'.
def verify_input_sanitization(input_string,input_type='none'):
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

    # Input is sanitary
    else:
        return True