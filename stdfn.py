# Standard sanitation of a given input. If the input is not valid in any
# way, return False. Otherwise, return True.
def sanitize_input(input):
    # Nonetype
    if input is None:
        return False
    # Empty string
    elif input == '':
        return False
    # Input is sanitary
    else:
        return True