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

    async def farm(self):
        """Send messages according to yaml config specifying frequency, channel, etc"""
        await self.client.wait_until_ready()

        while not self.client.is_closed:
            # Don"t proceed if no channels are configured
            if len(self.config["channels"]) == 0 or not self.config["enabled"]:
                if type(self.config["delay"]) is list:
                    # If the delay config option is a list, treat it as parameters
                    minmax = self.config["delay"]
                    # First parameter is the minimum, second is the maximum
                    await asyncio.sleep(self.rand.randint(minmax[0], minmax[1]))
                    continue

                # Wait for the configured amount of time before continuing
                await asyncio.sleep(self.config["delay"])
                continue

            channels = self.config["channels"]
            # If configured, shuffle the channels to randomize the order we farm them
            if self.config["randomchannels"]:
                self.rand.shuffle(channels)

            for schannel in channels:
                # Create a channel object of the configured channel id
                channel = discord.Object(id=schannel)
                # Send a random message in the configured channel
                message = await self.client.send_message(channel, self.rand.choice(self.config["messages"]))

                # If configured, delete messages after they are sent
                if self.config["silent"]:
                    # If configured, treat silent config option as parameters
                    if type(self.config["silent"]) is list:
                        minmax = self.config["silent"]
                        await asyncio.sleep(
                            # First parameter is the minimum, second is the maximum
                            self.rand.randint(minmax[0], minmax[1]))
                    else:
                        # If a static delay is configured, use it
                        if self.config["silent"] > 0:
                            await asyncio.sleep(self.config["silent"])

                    # Delete the message after any configured delays
                    await self.client.delete_message(message)

            # Delay the farming loop by the configured amount
            if isinstance(self.config["delay"], list):
                minmax = self.config["delay"]
                await asyncio.sleep(self.rand.randint(minmax[0], minmax[1]))
                continue

            await asyncio.sleep(self.config["delay"])

    async def rep(self):
        """Send messages to add rep to the configured person at a configured interval"""
        await self.client.wait_until_ready()

        # If disabled in configuration, don"t proceed
        if not self.config["enabled"] or not self.config["repfarming"]:
            return

        users = utils.user_generator(self.config["recipients"])

        while not self.client.is_closed:
            channel = discord.Object(id=self.config["repchannel"])

            # Send a message adding rep to the configured person
            await self.client.send_message(channel, f"t!rep <@{next(users)}>")

            # Delay the loop if configured
            if type(self.config["repdelay"]) is list:
                minmax = self.config["repdelay"]
                await asyncio.sleep(self.rand.randint(minmax[0], minmax[1]))
            else:
                await asyncio.sleep(self.config["repdelay"])
