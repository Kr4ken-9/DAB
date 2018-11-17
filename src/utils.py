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
