from src import utils, config


class SidneyConfig(config.Config):
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

        enabled = input("\nNow we will set up Sidney. Enter 'True' or 'False' to enable/disable sidneybot farming: ")
        enabled = utils.string_to_bool(enabled)
        yaml_conf["enabled"] = enabled

        if not enabled:
            print("Sidneybot farming disabled.")
            return yaml_conf

        work = input("\nEnter 'True' or 'False' to enable/disable work farming: ")
        work = utils.string_to_bool(work)
        yaml_conf["workfarming"] = work

        print("\nNow configure the interval at which work will be farmed, called delay.")
        delay = int(input("Enter the interval in seconds: "))
        yaml_conf["delay"] = int(delay)

        print("\nFinally, configure the channel to farm work in.")
        channel = input("Enter the id of the channel: ")
        yaml_conf["channel"] = int(channel)

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