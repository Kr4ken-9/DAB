import discord
import asyncio
import config


def handle_command(client, message, configs):
    """Check if incoming message is a command and handle it if it is.

    :param client: Farmer's discord client
    :param message: Incoming messasge
    :param configs: List of configurations
    """
    _config = configs[0]
    repconfig = configs[1]

    if message.author.id != client.user.id and message.author.id not in _config['owners']:
        return

    if message.author.id != client.user.id and message.content.startswith('|'):
        client.send_message(message.channel, message.content[1:])
        return

    if message.content.startswith('_add'):
        _config['channels'].append(message.channel.id)

    if message.content.startswith('_remove'):
        _config['channels'].remove(message.channel.id)

    if message.content.startswith('_save'):
        config.save_config('config.yaml', _config)
        config.save_config('repconfig.yaml', repconfig)