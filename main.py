import discord
from src import config
from src.tatsumaki import tatsumaki
from src.sushii import sushii

client = discord.Client()


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")


@client.event
async def on_message(message):
    """Check all incoming messages to see if they are commands, handle them if they are

    :param message: Incoming message
    """
    #commands.handle_command(client, message, [_config, repconfig])


tat = tatsumaki.Tatsumaki(client)
sush = sushii.Sushii(client)

client.loop.create_task(tat.farm())
client.loop.create_task(tat.rep())
client.loop.create_task(sush.rep())
client.loop.create_task(sush.fishy())

_config = config.Config("Configs/Shared.yaml").load_config()
client.run(_config["token"], bot=False)
