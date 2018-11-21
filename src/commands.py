def handle_command(client, message, config):
    """Check if incoming message is a command and handle it if it is.

    :param client: Farmer's discord client
    :param message: Incoming message
    :param config: YAML Configuration
    """

    if message.author.id != client.user.id and message.author.id not in config["owners"]:
        return

    if message.content.startswith("|"):
        client.send_message(message.channel, message.content[1:])
        return
