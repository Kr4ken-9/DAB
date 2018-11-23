import asyncio

class MessageHandler:
    def __init__(self, client, shared_config, pokecord):
        self.client = client
        self.shared_config = shared_config
        self.pokecord = pokecord

    async def handle_message(self, message):
        """Check if each incoming message is a command or something to be operated on

        :param message:
        :return:
        """

        # Check if message is a new pokemon and if so catch it
        if self.pokecord.pokecord_check(message):
            await self.pokecord.find_pokemon(message)

        # Check if message is a command
        owners = self.shared_config["owners"]
        if message.author.id != self.client.user.id and message.author.id not in owners:
            return

        if message.content.startswith("|"):
            message.channel.send(message.content[1:])
