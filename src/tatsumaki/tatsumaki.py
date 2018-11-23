import discord
import asyncio
import random
from src import utils
from src.tatsumaki import tatconfig


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

        users = utils.user_generator(self.config["recipients"])

        while not self.client.is_closed():
            channel = self.client.get_channel(self.config["channel"])

            # Get a random message from one of the configured ones
            random_message = f"t!rep <@{next(users)}>"

            # If configured, get the delay before deleting the message
            if self.config["silent"]:
                silent_delay = utils.get_delay(self.config["silent"], self.rand)

            # Send a random message in the configured channel
            if self.config["silent"]:
                await channel.send(random_message, delete_after=silent_delay)
            else:
                await channel.send(random_message)

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["delay"], self.rand))
