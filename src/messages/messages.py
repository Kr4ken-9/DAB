import discord
import asyncio
import random
from src import utils
from src.messages import messagesconfig


class Messages:
    def __init__(self, client):
        self.client = client
        m = messagesconfig.MessagesConfig("Configs/Messages.yaml")
        self.config = m.load_config()
        self.rand = random.SystemRandom()

    async def farm(self):
        """Send messages according to yaml config specifying frequency, channel, etc"""
        await self.client.wait_until_ready()

        while not self.client.is_closed:
            # Don"t proceed if no channels are configured
            if len(self.config["channels"]) == 0 or not self.config["enabled"]:
                return

            channels = self.config["channels"]
            # If configured, shuffle the channels to randomize the order we farm them
            if self.config["randomchannels"]:
                self.rand.shuffle(channels)

            for schannel in channels:
                # Create a channel object of the configured channel id
                channel = discord.Object(id=schannel)
                # Send a random message in the configured channel
                message = await self.client.send_message(channel, self.rand.choice(self.config["messages"]))

                # Wait for any configured delays before deleting the message, if configured
                if self.config["silent"]:
                    await asyncio.sleep(utils.get_delay(self.config["silent"], self.rand))
                    await self.client.delete_message(message)

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["delay"], self.rand))
