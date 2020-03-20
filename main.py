import discord
from discord.ext import commands
from src import config, message_handler
from src.tatsumaki import tatsumaki
from src.sushii import sushii
from src.messages import messages
from src.pokecord import pokecord
from src.sidney import sidney


class DAB(commands.bot.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix=command_prefix, self_bot=True)
        self.messages = messages.Messages(self)
        self.tatsumaki = tatsumaki.Tatsumaki(self)
        self.sushii = sushii.Sushii(self)
        self.pokecord = pokecord.Pokecord(self)
        self.sidney = sidney.Sidney(self)
        self.shared = shared_yaml
        self.MessageHandler = message_handler.MessageHandler(self)

        self.start_background_tasks()

    def start_background_tasks(self):
        self.loop.create_task(self.messages.farm())
        self.loop.create_task(self.tatsumaki.rep())
        self.loop.create_task(self.sushii.rep())
        self.loop.create_task(self.sushii.fishy())
        self.loop.create_task(self.sidney.work())

    async def on_ready(self):
        print("\nLogged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")

    async def on_message(self, message):
        await self.MessageHandler.handle_message(message)


shared = config.Config("Configs/Shared.yaml")
shared_yaml = shared.load_config()

client = DAB(command_prefix=shared_yaml["prefix"])

client.load_extension("src.COMMANDS")
client.run(shared_yaml["token"], bot=False)
