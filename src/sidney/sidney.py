import asyncio
import random

from src import utils, outbound_message
from src.sidney import sidneyconfig


class Sidney:
    def __init__(self, client):
        self.client = client
        s = sidneyconfig.SidneyConfig("Configs/Sidney.yaml")
        self.config = s.load_config()
        self.rand = random.SystemRandom()

    async def work(self):
        """Automate working for Sidneybot with a configured interval"""
        await self.client.wait_until_ready()

        if self.client.shared["logging"]:
            utils.log("Sidneybot work farming enabled")

        channel = self.client.get_channel(self.config["channel"])

        while not self.client.is_closed():
            # Human typing delay
            typing_delay = self.rand.randint(1, 3)

            # Farm work
            outbound = outbound_message.Outbound_Message("sid work", channel, typing_delay)
            await outbound.send()

            if self.client.shared["logging"]:
                utils.log(f"Farmed Sidneybot work in {channel.id}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["delay"], self.rand))
