import discord
import asyncio
import yaml
import random

client = discord.Client()

rand = random.SystemRandom()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('_add'):
        config['channels'].append(message.channel.id)

    if message.content.startswith('_remove'):
        config['channels'].remove(message.channel.id)

    if message.content.startswith('_save'):
        with open('config.yaml', 'w') as file:
            file.write(yaml.dump(config))

async def farm():
    await client.wait_until_ready()

    while not client.is_closed:
        if len(config['channels']) == 0:
            await asyncio.sleep(config['delay'])
            return

        for schannel in config['channels']:
            channel = discord.Object(id=schannel)
            message = await client.send_message(channel, rand.choice(config['messages']))

            if config['silent']:
                await client.delete_message(message)

            await asyncio.sleep(config['delay'])

with open('config.yaml', 'r') as file:
    config = yaml.load(file)

client.loop.create_task(farm())
client.run(config['token'], bot=False)
