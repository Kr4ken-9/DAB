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
    if message.author.id != client.user.id and message.author.id not in config['owners']:
        return

    if message.author.id != client.user.id and message.content.startswith('|'):
        await client.send_message(message.channel, message.content[1:])
        return

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
            if type(config['delay']) is list:
                minmax = config['delay']
                await asyncio.sleep(rand.randint(minmax[0], minmax[1]))
                continue

            await asyncio.sleep(config['delay'])
            continue

        channels = config['channels']
        if config['randomchannels']:
            rand.shuffle(channels)

        for schannel in channels:
            channel = discord.Object(id=schannel)
            message = await client.send_message(channel, rand.choice(config['messages']))

            if config['silent']:
                if type(config['silent']) is list:
                    minmax = config['silent']
                    await asyncio.sleep(rand.randint(minmax[0], minmax[1]))
                else:
                    if config['silent'] > 0:
                        await asyncio.sleep(config['silent'])

                await client.delete_message(message)

        if type(config['delay']) is list:
            minmax = config['delay']
            await asyncio.sleep(rand.randint(minmax[0], minmax[1]))
            continue

        await asyncio.sleep(config['delay'])


with open('config.yaml', 'r') as file:
    config = yaml.load(file)

#client.loop.create_task(farm())
client.run(config['token'], bot=False)
