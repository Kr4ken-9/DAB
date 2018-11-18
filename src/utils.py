import random


def __string_to_bool(string):
    if string == "TRUE":
        return True
    elif string == "FALSE":
        return False
    else:
        raise ValueError("String is not true or false (not a boolean)")


def string_to_bool(string):
    supper = string.upper()

    try:
        return __string_to_bool(supper)
    except ValueError:
        return string


def user_generator(users):
        random.shuffle(users)
        c = 0
        while True:
            yield users[c]
            c += 1
            if c >= len(users):
                c = 0


def get_delay(config, rand):
    # If configured, treat silent config option as parameters
    if type(config) is list:
        minmax = config

        # First parameter is the minimum, second is the max
        # Choose a random number between the min and max, and return as the delay
        return rand.randint(minmax[0], minmax[1])
    else:
        # If a static delay is configured, return it
        return config
