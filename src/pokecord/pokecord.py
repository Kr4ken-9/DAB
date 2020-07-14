import random
import asyncio
import datetime

import requests
from io import BytesIO
from PIL import Image
import imagehash
import json

from src import utils, outbound_message
from src.pokecord import pokeconfig


def load_json(path):
    with open(path, "r") as file:
        return json.load(file)


class Pokecord:
    def __init__(self, client):
        self.client = client
        p = pokeconfig.PokeConfig(f"{self.client.config_directory}/Pokecord.yaml")
        self.config = p.load_config()
        self.rand = random.SystemRandom()
        self.hashes = load_json("pokebois.json")
        self.pokebois = {}
        # Create case insensitive version of whitelist and blacklist lists
        # Can't trust anybody to capitalize lol
        self.whitelist = map(str.upper, self.config["whitelist"])
        self.blacklist = map(str.upper, self.config["blacklist"])
        self.lastinterval = None
        self.lastwait = None
        self.waiting = False

        # Convert saved hash strings to usable ImageHash objects
        self.hashes = {}
        hashes = load_json("pokebois.json")
        for key, value in hashes.items():
            self.hashes[imagehash.hex_to_hash(key)] = value

    # region checks

    def pokecord_check(self, message):
        # If the message is coming from a channel not configured, ignore
        if message.channel.id not in self.config["channels"]:
            return False

        # Check if DAB is configured to analyze these messages
        if self.config["pokecordclone"] and message.author.id == 665301904791699476:
            return True

        if self.config["poketwo"] and message.author.id == 716390085896962058:
            return True

        return False

    def check_catch(self, message):
        if len(message.mentions) != 1:
            return False

        if message.mentions[0].id != self.client.user.id:
            return False

        return True

    def check_other_catch(self, message):
        # Check if the pokecord message is congratulating someone for catching a pokemon
        if message.content[:15] != "Congratulations":
            return

        # Check if someone is mentioned
        if len(message.mentions) != 1:
            return

        # If the person is not us, update our pokebois dictionary so we do not catch a pokemon late
        if message.mentions[0].id != self.client.user.id:
            self.pokebois[message.channel.id] = "Caught"

    # endregion

    async def find_pokemon(self, message):
        """Filter messages to find catchable pokemon, and catch them

        :param message: Message to check for pokemon
        :return:
        """

        if self.config["intervalcatching"]:
            now = datetime.datetime.now()

            if self.lastinterval is None:
                self.lastinterval = now

            if self.waiting is False:
                if (now - self.lastinterval).total_seconds() >= (self.config["interval"])[0]:
                    self.lastwait = now
                    self.waiting = True

                    if self.client.shared["logging"]:
                        utils.log("Waiting configured interval before continuing to catch")
                    return False
            else:
                if (now - self.lastwait).total_seconds() >= (self.config["interval"])[1]:
                    self.waiting = False
                    self.lastinterval = now

                    if self.client.shared["logging"]:
                        utils.log("Autocatching resumed")
                else:
                    return False

        # If the message doesn't have an embed, ignore
        if len(message.embeds) != 1:
            self.check_other_catch(message)
            return False

        embed = message.embeds[0]

        # If the message isn't a catchable pokemon, ignore
        if not embed.title == "A wild pokémon has аppeаred!":  # Thank you hidden characters
            return False

        # Download the image (picture of pokemon)
        embedimage = embed.image
        url = embedimage.url
        image = requests.get(url)

        # Get pokemon from image
        success, pokemon = await self.hash(Image.open(BytesIO(image.content)))
        if success is False:
            utils.log(f"ERROR - Pokemon missing from database. Hash:\n{pokemon}\nPlease report this to https://github.com/Kr4ken-9/DAB/issues\nPlease include pokemon name in report!")
            return

        await self.catch(message.channel, pokemon)

    async def hash(self, png):
        """Create a perceptual hash and find a matching Pokemon"""
        # Remove the alpha channel that the pokecord clone messes with
        filtered_image = utils.alpharemover(png)

        # Create a 16-bit perceptual hash of the image
        hash = imagehash.dhash(filtered_image, 16)

        # Find a closely matching image from our hashes database
        # We use 15 as the threshold (Most are within 7-8)
        for key in self.hashes:
            if key - hash < 15:
                return True, str(self.hashes[key])

        # If there were no matches within our threshold, return False
        return False, str(hash)

    async def catch(self, channel, pokemon):
        """Catch that pokeman and release it if it's garbage

        :param channel: Channel to catch the pokemon in
        :param pokemon: Name of the pokemon to catch
        """

        # We use the uppercase verison of the pokemon a lot
        # So we will just create a variable for it here
        pupper = pokemon.upper()

        # Record latest pokemon that appeared in this channel
        self.pokebois[channel.id] = pupper

        # If whitelist is enabled, check if the pokemon we are trying to catch is whitelisted
        # If not, we're going to abort and not catch the pokemon
        if self.config["enablewhitelist"]:
            if pupper not in self.whitelist:
                if self.client.shared["logging"]:
                    utils.log(f"{pokemon} ignored, not whitelisted. Channel: {channel.id}")

                return

        # If blacklist is enabled, check if the pokemon we are trying to catch is blacklisted
        # If it is, we're going to abort and not catch the pokemon
        if self.config["enableblacklist"]:
            if pupper in self.blacklist:
                if self.client.shared["logging"]:
                    utils.log(f"{pokemon} ignored, blacklisted. Channel: {channel.id}")

                return

        # If configured, make pokemon name lowercase when we claim it
        # The idea is that it might look more human since we are presumably typing fast
        if self.config["lowercasepokemon"]:
            pokemon = pokemon.lower()

        # Get the prefix for this channel
        prefixes = self.config["prefixes"]
        prefix = prefixes[channel.id]

        async with channel.typing():
            # Wait for any configured delays before catching the pokemon
            await asyncio.sleep(utils.get_delay(self.config["autocatchdelay"], self.rand))

            # Check if the latest pokemon is still the one we are trying to catch
            # If not, this means someone has already caught it or a new one appeared
            # In which case we need to abort
            if self.pokebois[channel.id] != pupper:
                if self.client.shared["logging"]:
                    utils.log(f"{pokemon} was caught/replaced in {channel.id}")

                return

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
            # Wait for a minute so that we don't get cock blocked by pokecord cooldowns
            delay = utils.get_delay(self.config["autocatchdelay"], self.rand)

            # Get info on the pokeboi we just caught
            outbound = outbound_message.Outbound_Message(f"{prefix}info latest", channel, delay)
            await outbound.send()

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

        # Wait for a minute so that we don't get cock blocked by pokecord cooldowns
        delay = utils.get_delay(self.config["autocatchdelay"], self.rand)

        # Release that garbage pokeman
        outbound = outbound_message.Outbound_Message(f"{prefix}release {pokeman_number}", reply.channel, delay)
        await outbound.send()
        
        # More cooldowns
        delay = utils.get_delay(self.config["autocatchdelay"], self.rand)

        # Confirm you have standards
        outbound = outbound_message.Outbound_Message(f"{prefix}confirm", reply.channel, delay)
        await outbound.send()

        return True
