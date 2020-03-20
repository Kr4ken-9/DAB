import random
import asyncio

import requests
from io import BytesIO
from PIL import Image
import imagehash
import json

from src import utils
from src.pokecord import pokeconfig


def load_json(path):
    with open(path, "r") as file:
        return json.load(file)


class Pokecord:
    def __init__(self, client):
        self.client = client
        p = pokeconfig.PokeConfig("Configs/Pokecord.yaml")
        self.config = p.load_config()
        self.rand = random.SystemRandom()
        self.hashes = load_json("pokebois.json")

    def pokecord_check(self, message):
        # If the message is coming from a channel not configured, ignore
        if message.channel.id not in self.config["channels"]:
            return False

        # If the message isn't send by Pokecord bot, ignore
        if not message.author.id == 365975655608745985:
            return False

        return True

    def check_catch(self, message):
        if len(message.mentions) != 1:
            return False

        if message.mentions[0].id != self.client.user.id:
            return False

        return True

    async def find_pokemon(self, message):
        """Filter messages to find catchable pokemon, and catch them

        :param message: Message to check for pokemon
        :return:
        """
        await self.client.wait_until_ready()

        # If disabled, return
        if not self.config["enabled"] or not self.config["autocatch"]:
            return

        # If the message doesn't have an embed, ignore
        if len(message.embeds) != 1:
            return False

        embed = message.embeds[0]

        # If the message isn't a catchable pokemon, ignore
        if not embed.title == "‌‌A wild pokémon has аppeаred!": #Thank you hidden characters
            return

        # Download the image (picture of pokemon)
        embedimage = embed.image
        url = embedimage.url
        image = requests.get(url)

        # Pass image and channel to catch method
        await self.catch(message.channel, Image.open(BytesIO(image.content)))

    async def catch(self, channel, png):
        """Catch that pokeman and release it if it's garbage

        :param channel: Channel to catch the pokemon in
        :param png: Image to identify
        """
        # Create a perceptual difference hash of the image
        # A hash is just an identifier
        # Perceptual is how the image looks
        # Difference is a type of algorithm
        # Altogether: An identifier for how the image looks
        hash = str(imagehash.dhash(png))

        # Search through the list of hashes we already have for a match
        # The dictionary has keys of hashes and values of names
        # So we pass the hash and get the name of the Pokemon
        pokemon = self.hashes[hash]

        # Get the prefix for this channel
        prefixes = self.config["prefixes"]
        prefix = prefixes[channel.id]

        # Humans don't send messages instantly
        async with channel.typing():
            # Wait for any configured delays before catching the pokemon
            await asyncio.sleep(utils.get_delay(self.config["autocatchdelay"], self.rand))

            # Catch the pokemon
            await channel.send(f"{prefix}catch {pokemon}")

        # Next message should be a success message from Pokecord
        catch_or_fail = await self.client.wait_for("message", check=self.pokecord_check)

        caught = self.check_catch(catch_or_fail)

        if not caught:
            if self.client.shared["logging"]:
                utils.log(f"Failed to catch {pokemon} in {channel.id}")

            return

        if self.client.shared["logging"]:
            utils.log(f"Caught {pokemon} in {channel.id}")

        # If configured, determine whether this pokeboi is worthy of keeping or not
        if self.config["autorelease"]:
            # Humans don't send messages instantly
            async with channel.typing():
                # Wait for a minute so that we don't get cock blocked by pokecord cooldowns
                await asyncio.sleep(utils.get_delay(self.config["autocatchdelay"], self.rand))

                # Get info on the pokeboi we just caught
                await channel.send(f"{prefix}info latest")

            # Process the pokecord reply
            if await self.release(prefix):
                if self.client.shared["logging"]:
                    utils.log(f"Released {pokemon} in {channel.id}")

    async def release(self, prefix):
        """Release that garbage pokeman

        :param prefix: Prefix for the channel you caught that pokeman in
        """
        # Get the pokecord reply with our pokeboi info
        reply = await self.client.wait_for("message", check=self.pokecord_check)

        # If the message doesn't have an embed, ignore
        if len(reply.embeds) != 1:
            if self.client.shared["logging"]:
                utils.log("Failed to autorelease (no embeds)")

            return False

        # Get the embed where all the info is
        embed = reply.embeds[0]

        # Get the Total IV of the new pokeboi
        IV = utils.get_IV(embed)

        if float(IV) > self.config["minimumiv"]:
            return False

        pokeman_number = utils.get_pokeman_number(embed)

        # Humans still don't type instantly
        async with reply.channel.typing():
            # Wait for a minute so that we don't get cock blocked by pokecord cooldowns
            await asyncio.sleep(utils.get_delay(self.config["autocatchdelay"], self.rand))

            # Release that garbage pokeman
            await reply.channel.send(f"{prefix}release {pokeman_number}")

        # I'm starting to wonder, is humanity worth it?
        async with reply.channel.typing():
            # MORE POKECORD COOLDOWNS
            await asyncio.sleep(utils.get_delay(self.config["autocatchdelay"], self.rand))

            # Confirm you have standards
            await reply.channel.send(f"{prefix}confirm")

        return True
