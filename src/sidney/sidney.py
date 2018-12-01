import discord
import asyncio
import random
from src import utils
from src.sidney import sidneyconfig


class Sidney:
    def __init__(self, client):
        self.client = client
        s = sidneyconfig.SidneyConfig("Configs/Sidney.yaml")
        self.config = s.load_config()
        self.rand = random.SystemRandom()

    async def work(self):
        """Send messages to add work to the configured person at a configured interval"""
        await self.client.wait_until_ready()

        # If disabled in configuration, don"t proceed
        if not self.config["enabled"] or not self.config["workfarming"]:
            return

        if self.client.shared["logging"]:
            utils.log("Sidneybot work farming enabled")

        while not self.client.is_closed():
            channel = self.client.get_channel(self.config["channel"])

            # Farm work
            await channel.send("sid work")

            if self.client.shared["logging"]:
                utils.log(f"Farmed Sidneybot work in {channel.id}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["delay"], self.rand))
