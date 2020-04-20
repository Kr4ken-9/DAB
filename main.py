import argparse
import asyncio
import random

from discord.ext import commands

from src import config, message_handler
from src.messages import messages
from src.pokecord import pokecord
from src.sidney import sidney
from src.sushii import sushii
from src.tatsumaki import tatsumaki
from src.kohaipp import kohaipp


class DAB(commands.bot.Bot):
    def __init__(self, _onfig_directory, command_prefix):
        super().__init__(command_prefix=command_prefix, self_bot=True, fetch_offline_members=False)
        self.config_directory = config_directory
        self.rand = random.SystemRandom()

        self.messages = messages.Messages(self)
        self.tatsumaki = tatsumaki.Tatsumaki(self)
        self.sushii = sushii.Sushii(self)
        self.pokecord = pokecord.Pokecord(self)
        self.sidney = sidney.Sidney(self)
        self.kohaipp = kohaipp.Kohaipp(self)
        self.shared = shared_yaml
        self.MessageHandler = message_handler.MessageHandler(self)

    async def start_background_tasks(self):
        # Check if message farming is enabled and channels are configured
        if self.messages.config["enabled"]:
            if len(self.messages.config["channels"]) > 0:
                self.loop.create_task(self.messages.farm())

        # Check if rep farming is enabled
        if self.tatsumaki.config["repfarming"]:
            await asyncio.sleep(self.rand.randint(6, 7))
            self.loop.create_task(self.tatsumaki.rep())

        # Check if rep farming is enabled
        if self.sushii.config["repfarming"]:
            await asyncio.sleep(self.rand.randint(6, 7))
            self.loop.create_task(self.sushii.rep())

        # Check if fishy farming is enabled
        if self.sushii.config["fishyfarming"]:
            await asyncio.sleep(self.rand.randint(6, 7))
            self.loop.create_task(self.sushii.fishy())

        # Check if work farming is enabled
        if self.sidney.config["workfarming"]:
            await asyncio.sleep(self.rand.randint(6, 7))
            self.loop.create_task(self.sidney.work())

        if self.kohaipp.config["enabled"]:
            # Check if begging automation is enabled
            if self.kohaipp.config["begging"]:
                await asyncio.sleep(self.rand.randint(6, 7))
                self.loop.create_task(self.kohaipp.beg())

            # Check if raiding automation is enabled
            if self.kohaipp.config["raiding"]:
                await asyncio.sleep(self.rand.randint(6, 7))
                self.loop.create_task(self.kohaipp.raid())

            # Check if mining automation is enabled
            if self.kohaipp.config["mining"]:
                await asyncio.sleep(self.rand.randint(6, 7))
                self.loop.create_task(self.kohaipp.mine())

            # Check if bonding automation is enabled
            if self.kohaipp.config["bonding"]:
                await asyncio.sleep(self.rand.randint(6, 7))
                self.loop.create_task(self.kohaipp.bond())

    async def on_ready(self):
        print("\nLogged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")

        await self.start_background_tasks()

    async def on_message(self, message):
        await self.MessageHandler.handle_message(message)


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", required=False, help="Optional directory to read YAML configs from")
args = parser.parse_args()

config_directory = "Configs"
if args.config:
    config_directory = args.config

shared = config.Config(f"{config_directory}/Shared.yaml")
shared_yaml = shared.load_config()

client = DAB(config_directory, shared_yaml["prefix"])

client.load_extension("src.COMMANDS")
client.run(shared_yaml["token"], bot=False)
