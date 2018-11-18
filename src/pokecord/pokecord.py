import discord
import asyncio
import random
import json
from src import utils
from src.pokecord import pokeconfig


class Pokecord:
    def __init__(self, client):
        self.client = client
        p = pokeconfig.PokeConfig("Configs/Pokecord.yaml")
        self.config = p.load_config()
        self.rand = random.SystemRandom()

    async def find_pokemon(self, message):
        await self.client.wait_until_ready()

        if not self.config["enabled"] or not self.config["autocatch"]:
            return

        if message.channel.id not in self.config["channels"]:
            return

        if not message.author.id == '365975655608745985':
            return

        if len(message.embeds) != 1:
            return

        json = message.embeds[0]

    async def catch(self):
        """Send messages to add rep to the configured person at a configured interval"""
        await self.client.wait_until_ready()

        # If disabled in configuration, don"t proceed
        if not self.config["repfarming"]:
            return

        users = utils.user_generator(self.config["recipients"])

        while not self.client.is_closed:
            channel = discord.Object(id=self.config["channel"])

            # Send a message adding rep to the configured person
            message = await self.client.send_message(channel, f"t!rep <@{next(users)}>")

            # Wait for any configured delays before deleting the message, if configured
            if self.config["silent"]:
                await asyncio.sleep(utils.get_delay(self.config["silent"], self.rand))

                # Delete the message after any configured delays
                await self.client.delete_message(message)

            # Delay the loop if configured
            await asyncio.sleep(utils.get_delay(self.config["delay"], self.rand))
