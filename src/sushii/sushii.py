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
            message = await self.client.send_message(channel, f"-rep <@{next(users)}>")

            # Wait for any configured delays before deleting the message, if configured
            if self.config["silent"]:
                await asyncio.sleep(utils.get_delay(self.config["silent"], self.rand))

                # Delete the message after any configured delays
                await self.client.delete_message(message)

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["repdelay"], self.rand))

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
            message = await self.client.send_message(channel, f"-fishy <@{next(users)}>")

            # Wait for any configured delays before deleting the message, if configured
            if self.config["silent"]:
                await asyncio.sleep(utils.get_delay(self.config["silent"], self.rand))

                # Delete the message after any configured delays
                await self.client.delete_message(message)

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["fishydelay"], self.rand))
