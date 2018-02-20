# Standard sanitation of a given input. If the input is not valid in any
# way, return False. Otherwise, return True.
def verify_input_sanitization(input):
    # Nonetype
    if input is None:
        return False
    # Empty string
    elif input == '':
        return False
    # TODO: 4-16 characters ONLY
    # TODO: omit all non a-z0-9 chars (except .-_)
    # Input is sanitary
    else:
        return True