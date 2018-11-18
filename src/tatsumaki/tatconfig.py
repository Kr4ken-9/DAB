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

    def populate_config(self, yaml_conf):
        """Populates a new config with user input via commandline

        :param yaml_conf: An example config to replace values of
        :return: A populated config
        """

        print("\nNow we will set up Tatsumaki. If you would like to disable rep farming or configure it later, enter 'False' below.")
        recipient = input("However, if you would like to enable it, enter the id of the user you want to farm rep for: ")

        recipient = utils.string_to_bool(recipient)
        if not recipient:
            print("\nRep farming has been disabled.")
            yaml_conf["repfarming"] = recipient
            return yaml_conf

        recipients = []
        recipients.append(recipient)
        yaml_conf["recipients"] = recipients

        print("\nThe next configuration option is called silence.")
        print("Enter a number to remove farming messages after that amount in seconds.")
        print("You can manually configure TatsumakiFarmer later to delete messages after a random amount of time (See Documentation)")
        silent = input("Enter a number or 'False' to disable silence: ")
        silent = utils.string_to_bool(silent)

        # If user didn"t disable silence, convert it to integer
        if not isinstance(silent, bool):
            silent = int(silent)

        print("\nNow configure the interval at which rep will be farmed, called delay.")
        delay = int(input("Enter the interval in seconds: "))

        yaml_conf["delay"] = delay

        print("\nFinally, configure the channel to farm rep in.")
        channel = input("Enter the id of the channel: ")

        yaml_conf["channel"] = channel

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
