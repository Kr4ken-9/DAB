import asyncio
from src import utils


class MessageHandler:
    def __init__(self, bot):
        self.client = bot
        self.shared_config = bot.shared
        self.pokecord = bot.pokecord

    async def handle_message(self, message):
        """Check if each incoming message is a command or something to be operated on

        :param message:
        """

        # Check if message is a new pokemon and if so catch it
        if self.pokecord.pokecord_check(message):
            await self.pokecord.find_pokemon(message)
            return

        # Check if message is a command
        owners = self.shared_config["owners"]
        if message.author.id not in owners and message.author.id != self.client.user.id:
            return

        if message.content.startswith("|"):
            to_repeat = message.content[1:]

            # Type for a minute to look like a human
            async with message.channel.typing():
                await asyncio.sleep(self.rand.randint(1, 3))

                await message.channel.send(to_repeat)

            if self.shared_config["logging"]:
                utils.log(f"Repeated {to_repeat}")

            return

        await self.client.process_commands(message)  # https://discordpy.readthedocs.io/en/latest/faq.html#id18
