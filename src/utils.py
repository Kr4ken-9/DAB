import random
import datetime
from PIL import Image


# region stb
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


# endregion


# region pokecord
def get_IV(embed):
    # Get the description of the embed where all the info is
    description = embed.description

    # Get the index of the last place "%" occurs
    # The last time % appears is after it gives us the Total IV
    # So we can use this index to trim the description to just the Total IV
    index_of_last_percent = description.rfind("%")

    # Trim the description to just the Total IV
    IV = description[index_of_last_percent - 5:index_of_last_percent]

    return IV


def get_pokeman_number(embed):
    # Get the footer of the embed where the number of our pokeboi is
    footer = embed.footer

    # Get text of footer (That's the only thing in the footer lmao wtf)
    footer_text = footer.text

    # Get the index of "/" when it says "Pokeman: 69/420"
    # Only occurs once so we don't need fancy rfind
    index_of_slash_proportion = footer_text.find("/")

    # Get the index of ":" when it says "Pokeman: 69/420"
    # Again, only occurs once
    index_of_colon = footer_text.find(":")

    # Trim the footer to just the number of our new pokeboi
    pokeman_number = footer_text[index_of_colon + 2:index_of_slash_proportion]

    return pokeman_number


# endregion


def log(text):
    date = datetime.datetime.now()
    print(f"\n{date}: {text}")


def list_generator(list):
    """
    Create a randomized generator for a list
    :param list: List to be randomized
    :return: Randomized generator
    """
    random.shuffle(list)
    c = 0
    while True:
        yield list[c]
        c += 1
        if c >= len(list):
            random.shuffle(list)
            c = 0


def get_delay(config, rand):
    """
    Determine a delay based on YAML configuration
    :param config: YAML config element specifying a delay
    :param rand: Random object to return a random delay if configured
    :return: Randomized or specified delay as an integer
    """
    # If configured, treat silent config option as parameters
    if type(config) is list:
        minmax = config

        # First parameter is the minimum, second is the max
        # Choose a random number between the min and max, and return as the delay
        return rand.randint(minmax[0], minmax[1])
    else:
        # If a static delay is configured, return it
        return config


# New attempt at stopping DAB is doing some alpha channel fuckery to the background of images
# Turns out it doesn't work very well if we do some basic filtering
# Discussion and details here: https://github.com/Kr4ken-9/DAB/issues/62
# Stolen from here: https://github.com/JohannesBuchner/imagehash/blob/master/examples/hashimages.py#L18
def alpharemover(image):
    if image.mode != 'RGBA':
        return image
    canvas = Image.new('RGBA', image.size, (255,255,255,255))
    canvas.paste(image, mask=image)
    return canvas.convert('RGB')
