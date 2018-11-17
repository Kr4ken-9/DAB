import discord
import asyncio
import random
from src import utils
from src.sushii import sushiiconfig


class Sushii():
    def __init__(self, client):
        self.client = client
        self.rand = random.SystemRandom()
        s = sushiiconfig.Sushiiconfig("Configs/Sushii.yaml")
        self.config = s.load_config()

    async def rep(self):
        """Send messages to add rep to the configured person at a configured interval"""
        await self.client.wait_until_ready()

        # If disabled in configuration, don"t proceed
        if not self.config["repfarming"]:
            return

        users = utils.user_generator(self.config["reprecipients"])

        while not self.client.is_closed:
            channel = discord.Object(id=self.config["channel"])

            # Send a message adding rep to the configured person
            await self.client.send_message(channel, f"-rep <@{next(users)}>")

            # Delay the loop if configured
            if type(self.config["repdelay"]) is list:
                minmax = self.config["repdelay"]
                await asyncio.sleep(self.rand.randint(minmax[0], minmax[1]))
            else:
                await asyncio.sleep(self.config["repdelay"])

    async def fishy(self):
        """Send messages to add fishies to the configured person at a configured interval"""
        await self.client.wait_until_ready()

        # If disabled in configuration, don"t proceed
        if not self.config["fishyfarming"]:
            return

        users = utils.user_generator(self.config["fishyrecipients"])

        while not self.client.is_closed:
            channel = discord.Object(id=self.config["channel"])

            # Send a message adding fishies to the configured person
            await self.client.send_message(channel, f"-fishy <@{next(users)}>")

            # Delay the loop if configured
            if type(self.config["fishydelay"]) is list:
                minmax = self.config["fishydelay"]
                await asyncio.sleep(self.rand.randint(minmax[0], minmax[1]))
            else:
                await asyncio.sleep(self.config["fishydelay"])
