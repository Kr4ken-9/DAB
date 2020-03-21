import asyncio
import random

from src import utils
from src.tatsumaki import tatconfig
from src.messages import outbound_message


class Tatsumaki:
    def __init__(self, client):
        self.client = client
        t = tatconfig.Tatconfig("Configs/Tatsumaki.yaml")
        self.config = t.load_config()
        self.rand = random.SystemRandom()

    async def rep(self):
        """Send messages to add rep to the configured person at a configured interval"""
        await self.client.wait_until_ready()

        # If disabled in configuration, don"t proceed
        if not self.config["repfarming"]:
            return

        if self.client.shared["logging"]:
            utils.log("Tatsumaki rep farming enabled")

        recipients = utils.list_generator(self.config["recipients"])

        while not self.client.is_closed():
            channel = self.client.get_channel(self.config["channel"])

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
