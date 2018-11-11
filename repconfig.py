import config
import utils

def is_example(path):
    """Determines whether the given config file is an example

        :param path: Path to the config file
        :return: Whether or not the config file is an example
        """
    if config.check_config(path):
        c = config.load_config(path)

        if not c['recipients']:
            return False

        if c['channel'] == 435949310610374661:
            return True

        return False

    return True


def populate_config(yaml_conf):
    """Populates a new config with user input via commandline

        :param yaml_conf: An example config to replace values of
        :return: A populated config
        """

    print("Now we will setup the repconfig. If you would like to disable rep farming or configure it later, enter 'False' below.")
    recipient = input("However, if you would like to enable it, enter the id of the user you want to farm rep for: ")

    recipient = utils.string_to_bool(recipient)

    if not recipient:
        print("\nRep farming has been disabled.")
        yaml_conf['recipients'] = recipient
        return yaml_conf

    recipients = []
    recipients.append(recipient)
    yaml_conf['recipients'] = recipients

    print("\nNow configure the interval at which rep will be farmed, called delay.")
    delay = int(input("Enter the interval in seconds: "))

    yaml_conf['delay'] = delay

    print("\nFinally, configure the channel to farm rep in.")
    channel = input("Enter the id of the channel: ")

    yaml_conf['channel'] = channel

    return yaml_conf


def replace_example(path):
    """Replace example config with working config

    :param path: Path to example config
    """

    # Skip the config file if it's not an example
    if not is_example(path):
        return

    # Load the yaml of the example config
    oldconfig = config.load_config(path)

    # Replace example contents with working contents
    populated_config = populate_config(oldconfig)

    # Replace example config with working config
    config.save_config(path, populated_config)
