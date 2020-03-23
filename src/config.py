import yaml
import os


class Config:
    def __init__(self, path):
        self.path = path

    def check_config(self):
        """Check if config exists and is usable

        :return: Returns a bool representing whether the path exists and is a usable config
        """
        if not os.path.isfile(self.path):
            return False

        return True

    def save_config(self, newconfig):
        """Saves yaml config to path

            :param newconfig: Yaml config to save to path
            """
        with open(self.path, "w") as file:
            file.write(yaml.dump(newconfig))

    def load_config(self):
        """Loads path as a yaml config"""
        with open(self.path, "r") as file:
            return yaml.load(file, Loader=yaml.SafeLoader)

    def is_example(self):
        """Determines whether the given config file is an example

        :return: Whether or not the config file is an example
        """
        if self.check_config():
            c = self.load_config()

            return c["firsttime"]

        return True

    def populate_config(self, yaml_conf):
        pass

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
