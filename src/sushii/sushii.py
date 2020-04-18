import asyncio
import random

from src import utils, outbound_message
from src.sushii import sushiiconfig


class Sushii():
    def __init__(self, client):
        self.client = client
        self.rand = random.SystemRandom()
        s = sushiiconfig.Sushiiconfig("Configs/Sushii.yaml")
        self.config = s.load_config()

    async def rep(self):
        """Automate farming Sushii rep with a configured recipient and interval"""
        await self.client.wait_until_ready()

        if self.client.shared["logging"]:
            utils.log("Sushii rep farming enabled")

        recipients = utils.list_generator(self.config["reprecipients"])
        channel = self.client.get_channel(self.config["channel"])

        while not self.client.is_closed():
            # Get a random recipient from one of the configured ones
            random_recipient = next(recipients)

            # Human typing delay
            delay = self.rand.randint(1, 3)

            # Give the random recipient rep
            outbound = outbound_message.Outbound_Message(f"-rep <@{random_recipient}>", channel, delay)
            await outbound.send()

            if self.client.shared["logging"]:
                utils.log(f"Gave sushii rep to {random_recipient}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["repdelay"], self.rand))

    async def fishy(self):
        """Send messages to add fishies to the configured person at a configured interval"""
        await self.client.wait_until_ready()

        if self.client.shared["logging"]:
            utils.log("Sushii fishy farming enabled")

        recipients = utils.list_generator(self.config["fishyrecipients"])
        channel = self.client.get_channel(self.config["channel"])

        while not self.client.is_closed():
            # Get a random recipient from one of the configured ones
            random_recipient = next(recipients)

            # Human typing delay
            delay = self.rand.randint(1, 3)

            # Give the random recipient fishies
            outbound = outbound_message.Outbound_Message(f"-fishy <@{random_recipient}>", channel, delay)
            await outbound.send()

            if self.client.shared["logging"]:
                utils.log(f"Gave sushii fishies to {random_recipient}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["fishydelay"], self.rand))
