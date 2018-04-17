import discord
import asyncio
import yaml

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!ping'):
        await client.send_message(message.channel, 'pong')

    if message.content.startswith('_add'):
        channels.append(message.channel.id)

    if message.content.startswith('_remove'):
        channels.remove(message.channel.id)

async def farm():
    await client.wait_until_ready()

    while not client.is_closed:
        if len(channels) == 0:
            await asyncio.sleep(3)
            return

        for schannel in channels:
            channel = discord.Object(id=schannel)
            await client.send_message(channel, 'test')
            await asyncio.sleep(3)

with open('config.yaml', 'r') as file:
    config = yaml.load(file)

channels = config['channels']
client.loop.create_task(farm())
client.run(config['token'], bot=False)
