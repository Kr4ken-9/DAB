import discord
from src import config, commands
from src.tatsumaki import tatsumaki, tatconfig
from src.sushii import sushii, sushiiconfig
from src.messages import messages, messagesconfig
from src.pokecord import pokecord, pokeconfig

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
    #commands.handle_command(client, message, shared)

    if poke.pokecord_check(message):
        await poke.find_pokemon(message)


tat = tatsumaki.Tatsumaki(client)
sush = sushii.Sushii(client)
mess = messages.Messages(client)
poke = pokecord.Pokecord(client)

shared = config.Config("Configs/Shared.yaml")
tatconf = tatconfig.Tatconfig("Configs/Tatsumaki.yaml")
sushconf = sushiiconfig.Sushiiconfig("Configs/Sushii.yaml")
mconf = messagesconfig.MessagesConfig("Configs/Messages.yaml")
pokeconf = pokeconfig.PokeConfig("Configs/Pokecord.yaml")

mconf.replace_example()
tatconf.replace_example()
sushconf.replace_example()
pokeconf.replace_example()

client.loop.create_task(mess.farm())
client.loop.create_task(tat.rep())
client.loop.create_task(sush.rep())
client.loop.create_task(sush.fishy())
client.run(shared.load_config()["token"], bot=False)
