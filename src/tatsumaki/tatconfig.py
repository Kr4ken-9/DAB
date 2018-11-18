from src import utils, config


class Tatconfig(config.Config):
    def is_example(self):
        """Determines whether the given config file is an example

        :param path: Path to the config file
        :return: Whether or not the config file is an example
        """
        if self.check_config():
            c = self.load_config()

            return c["firsttime"]

        return True

    def save_token(self, token):
        sharedconfig = config.Config("Configs/Shared.yaml")
        newconfig = sharedconfig.load_config()
        newconfig["token"] = token

        sharedconfig.save_config(newconfig)

    def populate_config(self, yaml_conf):
        """Populates a new config with user input via commandline

        :param yaml_conf: An example config to replace values of
        :return: A populated config
        """

        print("This appears to be your first time running TatsumakiFarmer. Please populate the config manually or through these steps.")
        token = input("Enter the token: ")

        self.save_token(token)

        channels = []
        channels.append(input("\nEnter the channel id to farm in: "))

        print("\nThe next configuration option is called silence. Enter a negative number to instantly delete farming messages.")
        print("Enter a positive number to remove farming messages after that amount in seconds.")
        print("You can manually configure TatsumakiFarmer later to delete messages after a random amount of time (See Documentation)")
        silent = input("Enter a number or 'False' to disable silence: ")

        silent = utils.string_to_bool(silent)

        # If user didn"t disable silence, convert it to integer
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

        yaml_conf["firsttime"] = False
        yaml_conf["enabled"] = True
        yaml_conf["channels"] = channels
        yaml_conf["silent"] = silent
        yaml_conf["delay"] = delay
        yaml_conf["messages"] = messages
        yaml_conf["randomchannels"] = utils.string_to_bool(randomchannels)
        yaml_conf["owners"] = owners

        # End of regular farming, begin rep farming

        print("\nNow we will setup the repconfig. If you would like to disable rep farming or configure it later, enter 'False' below.")
        recipient = input("However, if you would like to enable it, enter the id of the user you want to farm rep for: ")

        recipient = utils.string_to_bool(recipient)

        if not recipient:
            print("\nRep farming has been disabled.")
            yaml_conf["repfarming"] = recipient
            return yaml_conf

        recipients = []
        recipients.append(recipient)
        yaml_conf["recipients"] = recipients

        print("\nNow configure the interval at which rep will be farmed, called delay.")
        repdelay = int(input("Enter the interval in seconds: "))

        yaml_conf["repdelay"] = repdelay

        print("\nFinally, configure the channel to farm rep in.")
        repchannel = input("Enter the id of the channel: ")

        yaml_conf["repchannel"] = repchannel

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
