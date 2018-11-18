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

        # firsttime: true
        # enabled: true
        # autocatch: true
        # prefix: 'p!'
        # channels: [513741591802806292]

        yaml_conf['firsttime'] = False

        print("\nIt appears you haven't configured pokecord farming yet. You can do so now or manually later.")
        enabled = input("Enter 'True' to enable pokecord farming and configure now, or 'False' for the opposite: ")

        yaml_conf["enabled"] = enabled

        autocatch = input("\nEnter 'True' or 'False' to enable/disable auto catching.: ")
        yaml_conf["autocatch"] = autocatch

        if not enabled:
            print("\nPokecord farming disabled.")
            return yaml_conf

        channels = []
        channels.append(input("\nEnter the channel id to farm in: "))

        prefixes = {}
        prefix = input("Enter the prefix for pokecord in that channel (default is p!): ")
        prefixes[channels[0]] = prefix
        yaml_conf["prefixes"] = prefixes

        print("\nThe next configuration option is called silence.")
        print("Enter a positive number to remove farming messages after that amount in seconds.")
        print("You can manually configure TatsumakiFarmer later to delete messages after a random amount of time (See Documentation)")
        silent = input("Enter a number or 'False' to disable silence: ")

        silent = utils.string_to_bool(silent)

        # If user didn"t disable silence, convert it to integer
        if not isinstance(silent, bool):
            silent = int(silent)

        yaml_conf["channels"] = channels
        yaml_conf["silent"] = silent

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
