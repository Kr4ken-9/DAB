import os
import yaml


def check_config(path):
    """Check if config exists and is usable

    :param path: Path to config
    :return: Returns a bool representing whether the path exists and is a usable config
    """
    if not os.path.isfile(path):
        return False

    config = yaml.load(path)
    if config['token'] == 'x':
        return False

    return True


def load_config(path):
    """Loads path as a yaml config

    :param path: Path to yaml config
    """
    with open(path, 'r') as file:
        return yaml.load(file)


def save_config(path, config):
    """Saves yaml config to path

    :param path: Path to save yaml config
    :param config: Yaml config to save to path
    """
    with open(path, 'w') as file:
        file.write(yaml.dump(config))
