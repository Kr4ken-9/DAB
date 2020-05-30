import asyncio
import datetime

import discord.utils
from discord.ext import commands
from src import utils, outbound_message


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.shared_config = client.shared
        # self.pokecord = client.pokecord

    # @commands.command(pass_context=True)
    # async def mrelease(self, context):
    #     prefixes = self.pokecord.config["prefixes"]

    #     # Calculate a human typing delay
    #     delay = self.pokecord.rand.randint(1, 3)

    #     outbound = outbound_message.Outbound_Message(f"{prefixes[context.channel.id]}pokemon", context.channel, delay)
    #     await outbound.send()

    #     reply = await self.client.wait_for("message", check=self.pokecord.pokecord_check)

    #     if len(reply.embeds) != 1:
    #         if self.shared_config["logging"]:
    #             utils.log("Something went wrong attempting to mass release pokemon (No embed)")

    #         return False

    #     embed = reply.embeds[0]

    #     if embed.title != "Your pokémon:":
    #         if self.shared_config["logging"]:
    #             utils.log("Something went wrong attempting to mass release pokemon (Incorrect embed)")

    #         return False

    #     print(f"\n\n{embed.description}\n\n")

    @commands.command(pass_context=True)
    async def clean(self, context, channel_id: int):
        channel = self.client.get_channel(channel_id)
        now = datetime.datetime.today()
        lastdate = discord.utils.snowflake_time(channel_id)
        messages = await channel.history(limit=9000, after=lastdate).flatten()

        while True:
            if lastdate >= now:
                break

            if len(messages) < 1:
                break

            for message in messages:
                if message.author.id != self.client.user.id:
                    continue

                await asyncio.sleep(.5)

                if self.shared_config["logging"]:
                    utils.log(f"Message: {message.content}")

                await message.delete()

            lastdate = messages[-1].created_at
            messages = await channel.history(limit=9000, after=lastdate).flatten()

        if self.shared_config["logging"]:
            utils.log(f"Command clean completed for {channel_id}")


def setup(client):
    client.add_cog(Commands(client))
