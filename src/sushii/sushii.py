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

        if self.client.shared["logging"]:
            utils.log("Sushii rep farming enabled")

        recipients = utils.list_generator(self.config["reprecipients"])

        while not self.client.is_closed():
            channel = self.client.get_channel(self.config["channel"])

            # Get a random recipient from one of the configured ones
            random_recipient = next(recipients)

            # If configured, get the delay before deleting the message
            if self.config["silent"]:
                silent_delay = utils.get_delay(self.config["silent"], self.rand)

            # Give the recipient rep
            async with channel.typing():
                await asyncio.sleep(self.rand.randint(1, 3))  # Also make it seem human

                if self.config["silent"]:
                    await channel.send(f"-rep <@{random_recipient}>", delete_after=silent_delay)
                else:
                    await channel.send(f"-rep <@{random_recipient}>")

            if self.client.shared["logging"]:
                utils.log(f"Gave sushii rep to {random_recipient}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["repdelay"], self.rand))

    async def fishy(self):
        """Send messages to add fishies to the configured person at a configured interval"""
        await self.client.wait_until_ready()

        # If disabled in configuration, don"t proceed
        if not self.config["fishyfarming"]:
            return

        if self.client.shared["logging"]:
            utils.log("Sushii fishy farming enabled")

        recipients = utils.list_generator(self.config["fishyrecipients"])

        while not self.client.is_closed():
            channel = self.client.get_channel(self.config["channel"])

            # Get a random recipient from one of the configured ones
            random_recipient = next(recipients)

            # If configured, get the delay before deleting the message
            if self.config["silent"]:
                silent_delay = utils.get_delay(self.config["silent"], self.rand)

            # Send a random message in the configured channel
            if self.config["silent"]:
                await channel.send(f"-fishy <@{random_recipient}>", delete_after=silent_delay)
            else:
                await channel.send(f"-fishy <@{random_recipient}>")

            if self.client.shared["logging"]:
                utils.log(f"Gave sushii fishies to {random_recipient}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["fishydelay"], self.rand))
