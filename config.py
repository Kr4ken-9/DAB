import os
import yaml
import utils


def check_config(path):
    """Check if config exists and is usable

    :param path: Path to config
    :return: Returns a bool representing whether the path exists and is a usable config
    """
    if not os.path.isfile(path):
        return False

    return True


def load_config(path):
    """Loads path as a yaml config

    :param path: Path to yaml config
    """
    with open(path, 'r') as file:
        return yaml.load(file)


def save_config(path, config):
    """Saves yaml config to path

    :param path: Path to save yaml config
    :param config: Yaml config to save to path
    """
    with open(path, 'w') as file:
        file.write(yaml.dump(config))


def is_example(path):
    """Determines whether the given config file is an example

    :param path: Path to the config file
    :return: Whether or not the config file is an example
    """
    if check_config(path):
        c = load_config(path)

        if c['token'] == 'x':
            return True

        return False

    return True


def populate_config(yaml_conf):
    """Populates a new config with user input via commandline

    :param yaml_conf: An example config to replace values of
    :return: A populated config
    """

    print("This appears to be your first time running TatsumakiFarmer. Please populate the config manually or through these steps.")
    token = input("Enter the token: ")

    channels = []
    channels.append(input("\nEnter the channel id to farm in: "))

    print("\nThe next configuration option is called silence. Enter a negative number to instantly delete farming messages.")
    print("Enter a positive number to remove farming messages after that amount in seconds.")
    print("You can manually configure TatsumakiFarmer later to delete messages after a random amount of time (See Documentation)")
    silent = input("Enter a number or 'False' to disable silence: ")

    silent = utils.string_to_bool(silent)

    # If user didn't disable silence, convert it to integer
    if not isinstance(silent, bool):
        silent = int(silent)

    print("\nThe next configuration option is delay. This is the interval in which farming messages are sent.")
    print("Delay can be configured manually to send messages at random intervals (See Documentation)")
    delay = int(input("Please enter a number (in seconds) in which messages will be sent: "))

    print("\nThe next configuration option is messages. Enter a message below that TatsumakiFarmer will use to farm.")
    print("This is an important option because some bots require a certain amount of characters to award points and such.")
    print("We will start with one message, you can later configure multiple (See Documentation)")
    messages = []
    messages.append(input("Enter a message: "))

    print("\nThis configuration option is simple. Called random channels, 'True' will cause it to send messages to configured channels in a random manner.")
    print("However, for this option to work, you must have manually configured multiple channels. 'False' will disable it.")
    randomchannels = input("Enter 'True' or 'False': ")

    print("\nFinally, configure an owner for TatsumakiFarmer. This will be a user's id (probably you) which will control the bot.")
    print("You can configure multiple owners manually (See Documentation)")
    owners = []
    owners.append(input("Enter the id: "))

    print("")

    yaml_conf['token'] = token
    yaml_conf['channels'] = channels
    yaml_conf['silent'] = silent
    yaml_conf['delay'] = delay
    yaml_conf['messages'] = messages
    yaml_conf['randomchannels'] = utils.string_to_bool(randomchannels)
    yaml_conf['owners'] = owners

    return yaml_conf


def replace_example(path):
    """Replace example config with working config

    :param path: Path to example config
    """

    # Skip the config file if it's not an example
    if not is_example(path):
        return

    # Load the yaml of the example config
    oldconfig = load_config(path)

    # Replace example contents with working contents
    populated_config = populate_config(oldconfig)

    # Replace example config with working config
    save_config(path, populated_config)