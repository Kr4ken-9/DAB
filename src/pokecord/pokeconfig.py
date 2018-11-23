from src import utils, config


class PokeConfig(config.Config):
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

        yaml_conf['firsttime'] = False

        print("\nIt appears you haven't configured pokecord farming yet. You can do so now or manually later.")
        enabled = input("Enter 'True' to enable pokecord farming and configure now, or 'False' for the opposite: ")

        yaml_conf["enabled"] = utils.string_to_bool(enabled)

        if not enabled:
            print("\nPokecord farming disabled.")
            return yaml_conf

        autocatch = input("\nEnter 'True' or 'False' to enable/disable auto catching: ")
        yaml_conf["autocatch"] = utils.string_to_bool(autocatch)

        autorelease = input("\nEnter 'True' or 'False' to enable/disable auto releasing based on IV%: ")
        yaml_conf["autorelease"] = utils.string_to_bool(autorelease)

        if autorelease:
            minimumiv = input("\nEnter the minimum IV% for incoming pokemon (Without the %): ")

            yaml_conf["minimumiv"] = int(minimumiv)

        print("\nNext, configure the autocatch delay. This is the delay between a pokemon appearing and when the bot catches it.")
        print("This can make the bot appear more legit since it's not immediately catching them.")
        autocatchdelay = input("Enter the delay, in seconds, for autocatch: ")
        yaml_conf["autocatchdelay"] = autocatchdelay

        channels = []
        channels.append(input("\nEnter the channel id to farm in: "))
        yaml_conf["channels"] = channels

        prefixes = {}
        prefix = input("Enter the prefix for pokecord in that channel (default is p!): ")
        prefixes[channels[0]] = prefix
        yaml_conf["prefixes"] = prefixes

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
