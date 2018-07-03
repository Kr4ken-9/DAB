import os
import yaml


def check_config(path):
    if not os.path.isfile(path):
        return False

    _config = load_config(path)
    if _config['token'] == 'x':
        return False

    return True


def load_config(path):
    with open(path, 'r') as file:
        return yaml.load(file)


def save_config(path, config):
    with open(path, 'w') as file:
        file.write(yaml.dump(config))

def assemble_config():
    token = input('Enter your token: ')
    repfarming = input('Would you like to enable rep farming? y/n ')

    repconfig = load_config('repconfig.yaml')
    config = load_config('config.yaml')

    if 'y' in repfarming:
        recipient = input('Enter the id of the user you would like to farm rep for: ')

        repconfig['recipients'] = [recipient]
    else:
        repconfig['recipients'] = False

    config['token'] = token
    save_config('config.yaml', config)
    save_config('repconfig.yaml', repconfig)
