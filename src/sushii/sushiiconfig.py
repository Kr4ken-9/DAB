from src import config, utils


class Sushiiconfig(config.Config):
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

        print("\nIt looks like you haven't configured options for sushiibot yet. You can do that now or manually later.")
        repfarming = input("The first option is to farm rep from sushiibot. Enter 'True' or 'False' regarding whether or not to farm sushii rep: ")
        repfarming = utils.string_to_bool(repfarming)
        yaml_conf["repfarming"] = repfarming

        fishyfarming = input("\nNow you can choose to farm fishies or not. Enter 'True' or 'False' to farm fishies: ")
        fishyfarming = utils.string_to_bool(fishyfarming)
        yaml_conf["fishyfarming"] = fishyfarming

        if not repfarming and not fishyfarming:
            print("\nAll sushiibot related farming is disabled.")
            return yaml_conf

        channel = input("Enter the channel id to farm sushii rep and fishies: ")

        silent = input("\nNow enter the delay, in seconds, before farming messages are deleted, or 'False' to disable deleting them: ")
        silent = utils.string_to_bool(silent)

        # If user didn't disable silence, convert it to integer
        if not isinstance(silent, bool):
            silent = int(silent)

        yaml_conf["silent"] = silent

        repdelay = input("\nNow enter the interval, in seconds, at which rep will be farmed: ")
        yaml_conf["repdelay"] = int(repdelay)

        fishydelay = input("\nNow enter the interval, in seconds, to farm fishies: ")
        yaml_conf["fishydelay"] = int(fishydelay)

        reprecipients = []
        print("\nThe next option is who to farm sushii rep for. You can manually configure multiple recipients later.")
        reprecipients.append(input("Enter the id of the user to farm rep for: "))
        yaml_conf["reprecipients"] = reprecipients

        fishyrecipients = []
        print("\nFinally, configure who to farm sushii fishies for. You can manually configure multiple recipients later.")
        fishyrecipients.append(input("Enter the id of the user to farm fishies for: "))
        yaml_conf["fishyrecipients"] = fishyrecipients

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
