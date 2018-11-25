import asyncio
from src import utils


class MessageHandler:
    def __init__(self, client):
        self.client = client
        self.shared_config = client.shared
        self.pokecord = client.pokecord

    async def handle_message(self, message):
        """Check if each incoming message is a command or something to be operated on

        :param message:
        :return:
        """

        # Check if message is a new pokemon and if so catch it
        if self.pokecord.pokecord_check(message):
            await self.pokecord.find_pokemon(message)
            return

        # Check if message is a command
        owners = self.shared_config["owners"]
        if message.author.id not in owners:
            return

        if message.content.startswith("|"):
            to_repeat = message.content[1:]
            await message.channel.send(to_repeat)

            if self.shared_config["logging"]:
                utils.log(f"Repeated {to_repeat}")
