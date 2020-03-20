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
