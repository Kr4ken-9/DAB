import asyncio
import random

from src import utils, outbound_message
from src.tatsumaki import tatconfig


class Tatsumaki:
    def __init__(self, client):
        self.client = client
        t = tatconfig.Tatconfig(f"{self.client.config_directory}/Tatsumaki.yaml")
        self.config = t.load_config()
        self.rand = random.SystemRandom()

    async def rep(self):
        """Automate farming Tatsumaki rep with a configured recipient and interval"""
        await self.client.wait_until_ready()

        if self.client.shared["logging"]:
            utils.log("Tatsumaki rep farming enabled")

        recipients = utils.list_generator(self.config["recipients"])
        channel = self.client.get_channel(self.config["channel"])

        while not self.client.is_closed():
            # Get a random recipient from one of the configured ones
            random_recipient = next(recipients)

            # Human typing delay
            delay = self.rand.randint(1, 3)

            # If configured, get the delay before deleting the message
            silent_delay = utils.get_delay(self.config["silent"], self.rand)

            # Give the recipient rep in the configured channel
            outbound = outbound_message.Outbound_Message(f"t!rep <@{random_recipient}>", channel, delay, silent_delay)
            await outbound.send()

            if self.client.shared["logging"]:
                utils.log(f"Gave tatsumaki rep to {random_recipient}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["delay"], self.rand))
