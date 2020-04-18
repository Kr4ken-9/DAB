from discord.ext import commands

from src import config, message_handler
from src.messages import messages
from src.pokecord import pokecord
from src.sidney import sidney
from src.sushii import sushii
from src.tatsumaki import tatsumaki
from src.kohaipp import kohaipp


class DAB(commands.bot.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix=command_prefix, self_bot=True, fetch_offline_members=False)
        self.messages = messages.Messages(self)
        self.tatsumaki = tatsumaki.Tatsumaki(self)
        self.sushii = sushii.Sushii(self)
        self.pokecord = pokecord.Pokecord(self)
        self.sidney = sidney.Sidney(self)
        self.kohaipp = kohaipp.Kohaipp(self)
        self.shared = shared_yaml
        self.MessageHandler = message_handler.MessageHandler(self)

        self.start_background_tasks()

    def start_background_tasks(self):
        # Check if message farming is enabled and channels are configured
        if self.messages.config["enabled"]:
            if len(self.messages.config["channels"]) > 0:
                self.loop.create_task(self.messages.farm())

        # Check if rep farming is enabled
        if self.tatsumaki.config["repfarming"]:
            self.loop.create_task(self.tatsumaki.rep())

        # Check if rep farming is enabled
        if self.sushii.config["repfarming"]:
            self.loop.create_task(self.sushii.rep())

        # Check if fishy farming is enabled
        if self.sushii.config["fishyfarming"]:
            self.loop.create_task(self.sushii.fishy())

        # Check if work farming is enabled
        if self.sidney.config["workfarming"]:
            self.loop.create_task(self.sidney.work())

        # Check if begging automation is enabled
        if self.kohaipp.config["begging"]:
            self.loop.create_task(self.kohaipp.beg())

        # Check if raiding automation is enabled
        if self.kohaipp.config["raiding"]:
            self.loop.create_task(self.kohaipp.raid())

        # Check if mining automation is enabled
        if self.kohaipp.config["mining"]:
            self.loop.create_task(self.kohaipp.mine())

        # Check if bonding automation is enabled
        if self.kohaipp.config["bonding"]:
            self.loop.create_task(self.kohaipp.bond())

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
