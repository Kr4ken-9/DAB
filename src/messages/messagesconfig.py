from src import utils, config


def save_shared(token, owners):
    sharedconfig = config.Config("Configs/Shared.yaml")
    newconfig = sharedconfig.load_config()
    newconfig["token"] = token
    newconfig["owners"] = owners

    sharedconfig.save_config(newconfig)


class MessagesConfig(config.Config):
    def __init__(self, path):
        super().__init__(path)

        self.replace_example()

    def is_example(self):
        """Determines whether the given config file is an example

        :param path: Path to the config file
        :return: Whether or not the config file is an example
        """
        if self.check_config():
            c = self.load_config()

            return c["firsttime"]

        return True

    def populate_config(self, yaml_conf):
        """Populates a new config with user input via commandline

        :param yaml_conf: An example config to replace values of
        :return: A populated config
        """

        yaml_conf["firsttime"] = False

        print("This appears to be your first time running DAB. Please populate the config manually or through these steps.")
        token = input("Enter the token: ")

        print("\nConfigure an owner for DAB. This will be a user's id (probably you) which will control the bot.")
        print("You can configure multiple owners manually (See Documentation)")
        owners = []
        owners.append(int(input("Enter the id: ")))
        save_shared(token, owners)

        enabled = input("Now, enter 'True' or 'False' to enable/disable message farming: ")
        enabled = utils.string_to_bool(enabled)
        yaml_conf["enabled"] = enabled

        if not enabled:
            print("\nMessage Farming disabled.")
            return yaml_conf

        channels = []
        channels.append(int(input("\nEnter the channel id to farm in: ")))
        yaml_conf["channels"] = channels

        print("\nThe next configuration option is called silence. Enter a positive number to remove farming messages after that amount in seconds.")
        print("You can manually configure DAB later to delete messages after a random amount of time (See Documentation)")
        silent = input("Enter a number or 'False' to disable silence: ")

        silent = utils.string_to_bool(silent)

        # If user didn"t disable silence, convert it to integer
        if not isinstance(silent, bool):
            silent = int(silent)

        yaml_conf["silent"] = silent

        print("\nThe next configuration option is delay. This is the interval in which farming messages are sent.")
        print("Delay can be configured manually to send messages at random intervals (See Documentation)")
        delay = int(input("Please enter a number (in seconds) in which messages will be sent: "))
        yaml_conf["delay"] = delay

        print("\nThe next configuration option is messages. Enter a message below that DAB will use to farm.")
        print("This is an important option because some bots require a certain amount of characters to award points and such.")
        print("We will start with one message, you can later configure multiple (See Documentation)")
        messages = []
        messages.append(input("Enter a message: "))
        yaml_conf["messages"] = messages

        print("\nFinally: Random Channels. 'True' will cause it to send messages to configured channels in a random manner.")
        print("However, for this option to work, you must have manually configured multiple channels. 'False' will disable it.")
        randomchannels = input("Enter 'True' or 'False': ")
        yaml_conf["randomchannels"] = utils.string_to_bool(randomchannels)

        return yaml_conf

    def replace_example(self):
        """Replace example config with working config"""

        # Skip the config file if it"s not an example
        if not self.is_example():
            return

        # Load the yaml of the example config
        oldconfig = self.load_config()

        # Replace example contents with working contents
        populated_config = self.populate_config(oldconfig)

        # Replace example config with working config
        self.save_config(populated_config)
