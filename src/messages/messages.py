import discord
import asyncio
import random
from src import utils
from src.messages import messagesconfig, outbound_message


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

            messages = utils.list_generator(self.config["messages"])

        while not self.client.is_closed():
            channels = self.config["channels"]
            # If configured, shuffle the channels to randomize the order we farm them
            if self.config["randomchannels"]:
                self.rand.shuffle(channels)

            for schannel in channels:
                # Create a channel object of the configured channel id
                channel = self.client.get_channel(schannel)

                # Get a random message from one of the configured ones
                random_message = next(messages)

                # Generate a human delay before sending the message
                delay = self.rand.randint(1, 3)

                # If configured, get the delay before deleting the message
                silent_delay = utils.get_delay(self.config["silent"], self.rand)

                # Send a random message in the configured channel
                outbound = outbound_message.Outbound_Message(random_message, channel, delay, silent_delay)
                await outbound.send()

                if self.client.shared["logging"]:
                    utils.log(f"Sent \"{random_message}\" to {schannel}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["delay"], self.rand))
