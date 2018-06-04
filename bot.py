import discord
import asyncio
import random
import config

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
    if message.author.id != client.user.id and message.author.id not in _config['owners']:
        return

    if message.author.id != client.user.id and message.content.startswith('|'):
        await client.send_message(message.channel, message.content[1:])
        return

    if message.content.startswith('_add'):
        _config['channels'].append(message.channel.id)

    if message.content.startswith('_remove'):
        _config['channels'].remove(message.channel.id)

    if message.content.startswith('_save'):
        config.save_config('config.yaml', _config)
        config.save_config('repcofnig.yaml', repconfig)


async def farm():
    await client.wait_until_ready()

    while not client.is_closed:
        if len(_config['channels']) == 0:
            if type(_config['delay']) is list:
                minmax = _config['delay']
                await asyncio.sleep(rand.randint(minmax[0], minmax[1]))
                continue

            await asyncio.sleep(_config['delay'])
            continue

        channels = _config['channels']
        if _config['randomchannels']:
            rand.shuffle(channels)

        for schannel in channels:
            channel = discord.Object(id=schannel)
            message = await client.send_message(channel, rand.choice(_config['messages']))

            if _config['silent']:
                if type(_config['silent']) is list:
                    minmax = _config['silent']
                    await asyncio.sleep(rand.randint(minmax[0], minmax[1]))
                else:
                    if _config['silent'] > 0:
                        await asyncio.sleep(_config['silent'])

                await client.delete_message(message)

        if type(_config['delay']) is list:
            minmax = _config['delay']
            await asyncio.sleep(rand.randint(minmax[0], minmax[1]))
            continue

        await asyncio.sleep(_config['delay'])

async def rep():
    await client.wait_until_ready()
    
    if not repconfig['recipients']:
        return
    
    users = user_generator(repconfig['recipients'])
    
    while not client.is_closed:
        channel = discord.Object(id=repconfig['channel'])
        await client.send_message(channel, f"t!rep <@{next(users)}>")

        if type(repconfig['delay']) is list:
            minmax = repconfig['delay']
            await asyncio.sleep(rand.randint(minmax[0], minmax[1]))
        else:
            await asyncio.sleep(repconfig['delay'])

def user_generator(users):
    random.shuffle(users)
    c = 0;
    while True:
        yield users[c]
        c += 1
        if c >= len(users):
            c = 0

_config = config.load_config('config.yaml')
repconfig = config.load_config('repconfig.yaml')

client.loop.create_task(farm())
client.loop.create_task(rep())

client.run(_config['token'], bot=False)
