import discord
from src import config, message_handler
from src.tatsumaki import tatsumaki
from src.sushii import sushii
from src.messages import messages
from src.pokecord import pokecord


class DAB(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = messages.Messages(self)
        self.tatsumaki = tatsumaki.Tatsumaki(self)
        self.sushii = sushii.Sushii(self)
        self.pokecord = pokecord.Pokecord(self)
        self.MessageHandler = message_handler.MessageHandler(self, shared.load_config(), self.pokecord)

        self.start_background_tasks()

    def start_background_tasks(self):
        self.loop.create_task(self.messages.farm())
        self.loop.create_task(self.tatsumaki.rep())
        self.loop.create_task(self.sushii.rep())
        self.loop.create_task(self.sushii.fishy())

    async def on_ready(self):
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")

    async def on_message(self, message):
        await self.MessageHandler.handle_message(message)


shared = config.Config("Configs/Shared.yaml")

client = DAB()
client.run(shared.load_config()["token"], bot=False)
