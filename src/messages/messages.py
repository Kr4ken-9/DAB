import asyncio
import random
from src import utils, outbound_message
from src.messages import messagesconfig


class Messages:
    def __init__(self, client):
        self.client = client
        m = messagesconfig.MessagesConfig(f"{self.client.config_directory}/Messages.yaml", self.client.config_directory)
        self.config = m.load_config()
        self.rand = random.SystemRandom()

    async def farm(self):
        """Automate sending messages with a configured frequency, channel, etc"""
        
        if self.client.shared["logging"]:
            utils.log("Message farming enabled")

        messages = utils.list_generator(self.config["messages"])
        channels = self.config["channels"]

        while not self.client.is_closed():
            # If configured, shuffle the channels to randomize the order we farm them
            if self.config["randomchannels"]:
                self.rand.shuffle(channels)

            for channel_id in channels:
                # Create a channel object of the configured channel id
                channel = self.client.get_channel(channel_id)

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
                    utils.log(f"Sent \"{random_message}\" to {channel_id}")

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["delay"], self.rand))
