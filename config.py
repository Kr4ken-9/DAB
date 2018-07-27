import os
import yaml


def check_config(path):
    if not os.path.isfile(path):
        return False

    config = yaml.load(path)
    if config['token'] == 'x':
        return False

    return True


def load_config(path):
    with open(path, 'r') as file:
        return yaml.load(file)


def save_config(path, config):
    with open(path, 'w') as file:
        file.write(yaml.dump(config))
