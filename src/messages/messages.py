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

        # Don"t proceed if no channels are configured or configured to
        if not self.config["enabled"] or len(self.config["channels"]) == 0:
            return

        if self.client.shared["logging"]:
            utils.log("Message farming enabled")

        while not self.client.is_closed():
            channels = self.config["channels"]
            # If configured, shuffle the channels to randomize the order we farm them
            if self.config["randomchannels"]:
                self.rand.shuffle(channels)

            for schannel in channels:
                # Create a channel object of the configured channel id
                channel = self.client.get_channel(schannel)

                # Get a random message from one of the configured ones
                random_message = self.rand.choice(self.config["messages"])

                # If configured, get the delay before deleting the message
                if self.config["silent"]:
                    silent_delay = utils.get_delay(self.config["silent"], self.rand)

                # Send a random message in the configured channel
                if self.config["silent"]:
                    await channel.send(random_message, delete_after=silent_delay)
                else:
                    await channel.send(random_message)

                if self.client.shared["logging"]:
                    # TODO: specify who
                    utils.log(f"Sent message to {schannel}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["delay"], self.rand))
