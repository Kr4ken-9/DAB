import asyncio
from discord.ext import commands
from src import utils


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.shared_config = client.shared
        self.pokecord = client.pokecord

    @commands.command(pass_context=True)
    async def mrelease(self, context):
        prefixes = self.pokecord.config["prefixes"]

        async with context.channel.typing():  # Humans need a minute


            await context.send(f"{prefixes[context.channel.id]}pokemon")

        reply = await self.client.wait_for("message", check=self.pokecord.pokecord_check)

        if len(reply.embeds) != 1:
            if self.shared_config["logging"]:
                utils.log("Something went wrong attempting to mass release pokemon (No embed)")

            return False

        embed = reply.embeds[0]

        if embed.title != "Your pokémon:":
            if self.shared_config["logging"]:
                utils.log("Something went wrong attempting to mass release pokemon (Incorrect embed)")

            return False

        print(f"\n\n{reply.embed.description}\n\n")


def setup(client):
    client.add_cog(Commands(client))
