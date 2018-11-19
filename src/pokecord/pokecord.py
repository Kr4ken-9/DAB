import random

import requests
from io import BytesIO
from PIL import Image
import imagehash
import json

from src import utils
from src.pokecord import pokeconfig


class Pokecord:
    def __init__(self, client):
        self.client = client
        p = pokeconfig.PokeConfig("Configs/Pokecord.yaml")
        self.config = p.load_config()
        self.rand = random.SystemRandom()
        self.hashes = self.load_json("pokebois.json")

    async def find_pokemon(self, message):
        """Filter messages to find catchable pokemon, and catch them

        :param message: Message to check for pokemon
        :return:
        """
        await self.client.wait_until_ready()

        # If disabled, return
        if not self.config["enabled"] or not self.config["autocatch"]:
            return

        # If the message is coming from a channel not configured, ignore
        if message.channel.id not in self.config["channels"]:
            return

        # If the message isn't send by Pokecord bot, ignore
        if not message.author.id == "365975655608745985":
            return

        # If the message doesn't have an embed, ignore
        if len(message.embeds) != 1:
            return

        embed = message.embeds[0]

        # If the message isn't a catchable pokemon, ignore
        if not embed["title"] == "‌‌A wild pokémon has appeared!":
            return

        # Download the image (picture of pokemon)
        embedimage = embed["image"]
        url = embedimage["url"]
        image = requests.get(url)

        # Pass image and channel to catch method
        await self.catch(message.channel, Image.open(BytesIO(image.content)))

    async def catch(self, channel, png):
        """

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

        # Catch the pokemon
        await self.client.send_message(channel, f";catch {pokemon}")

    @staticmethod
    def load_json(path):
        with open(path, "r") as file:
            return json.load(file)
