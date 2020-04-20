import asyncio
import random

from src import utils, outbound_message
from src.kohaipp import kohaippconfig


class Kohaipp():
    def __init__(self, client):
        self.client = client
        self.rand = random.SystemRandom()
        k = kohaippconfig.Kohaippconfig(f"{self.client.config_directory}/Kohaipp.yaml")
        self.config = k.load_config()

    async def beg(self):
        """Automate begging for Kohaipp gold with a configured channel"""

        if self.client.shared["logging"]:
            utils.log("Kohaipp begging enabled")

        channel = self.client.get_channel(self.config["begchannel"])

        while not self.client.is_closed():
            # Human typing delay
            delay = self.rand.randint(1, 2)

            # Beg!
            outbound = outbound_message.Outbound_Message("pp!b", channel, delay)
            await outbound.send()

            if self.client.shared["logging"]:
                utils.log(f"Kohaipp - Begged in {channel.id}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["begdelay"], self.rand))

    async def raid(self):
        """Automate raiding for Kohaipp with a configured channel"""

        if self.client.shared["logging"]:
            utils.log("Kohaiipp raiding enabled")

        channel = self.client.get_channel(self.config["raidchannel"])

        while not self.client.is_closed():
            # Human typing delay
            delay = self.rand.randint(1, 2)

            # Raid!
            outbound = outbound_message.Outbound_Message("pp!r", channel, delay)
            await outbound.send()

            if self.client.shared["logging"]:
                utils.log(f"Kohaipp - Raided in {channel.id}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["raiddelay"], self.rand))

    async def mine(self):
        """Automate mining for Kohaipp with a configured channel"""

        if self.client.shared["logging"]:
            utils.log("Kohaiipp mining enabled")

        channel = self.client.get_channel(self.config["minechannel"])

        while not self.client.is_closed():
            # Human typing delay
            delay = self.rand.randint(1, 2)

            # Mine!
            outbound = outbound_message.Outbound_Message("pp!m", channel, delay)
            await outbound.send()

            if self.client.shared["logging"]:
                utils.log(f"Kohaipp - Mined in {channel.id}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["minedelay"], self.rand))

    async def bond(self):
        """Automate bonding with your Kohaipp pet with a configured channel"""

        if self.client.shared["logging"]:
            utils.log("Kohaiipp pet bonding enabled")

        channel = self.client.get_channel(self.config["bondchannel"])

        while not self.client.is_closed():
            # Human typing delay
            delay = self.rand.randint(1, 2)

            # Bond!
            outbound = outbound_message.Outbound_Message("pp!petb", channel, delay)
            await outbound.send()

            if self.client.shared["logging"]:
                utils.log(f"Kohaipp - Bonded in {channel.id}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["bonddelay"], self.rand))
