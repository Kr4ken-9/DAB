import discord
import asyncio
import random
import config
import commands

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
    """Check all incoming messages to see if they are commands, handle them if they are

    :param message: Incoming message
    """
    commands.handle_command(client, message, [_config, repconfig])


async def farm():
    """Send messages according to yaml config specifying frequency, channel, etc"""
    await client.wait_until_ready()

    while not client.is_closed:
        if len(_config['channels']) == 0: # Don't proceed if no channels are configured
            if type(_config['delay']) is list:
                minmax = _config['delay'] # If the delay config option is a list, treat it as parameters
                await asyncio.sleep(rand.randint(minmax[0], minmax[1])) # First parameter is the minimum, second is the maximum
                continue

            await asyncio.sleep(_config['delay']) # Wait for the configured amount of time before continuing
            continue

        channels = _config['channels']
        if _config['randomchannels']: # If configured, shuffle the channels to randomize the order we farm them
            rand.shuffle(channels)

        for schannel in channels:
            channel = discord.Object(id=schannel) # Create a channel object of the configured channel id
            message = await client.send_message(channel, rand.choice(_config['messages'])) # Send a random message in the configured channel

            if _config['silent']: # If configured, delete messasges after they are sent
                if type(_config['silent']) is list: # If configured, treat silent config option as parameters
                    minmax = _config['silent']
                    await asyncio.sleep(rand.randint(minmax[0], minmax[1])) # First parameter is the minimum, second is the maximum
                else:
                    if _config['silent'] > 0: # If a static delay is configured, use it
                        await asyncio.sleep(_config['silent'])

                await client.delete_message(message) # Delete the message after any configured delays

        if type(_config['delay']) is list: # Delay the farming loop by the configured amount
            minmax = _config['delay']
            await asyncio.sleep(rand.randint(minmax[0], minmax[1]))
            continue

        await asyncio.sleep(_config['delay'])

async def rep():
    """Send messages to add rep to the configured person at a configured interval"""
    await client.wait_until_ready()
    
    if not repconfig['recipients']: # If disabled in configuration, don't proceed
        return
    
    users = user_generator(repconfig['recipients'])
    
    while not client.is_closed:
        channel = discord.Object(id=repconfig['channel'])
        await client.send_message(channel, f"t!rep <@{next(users)}>") # Send a message adding rep to the configured person

        if type(repconfig['delay']) is list: # Delay the loop if configured
            minmax = repconfig['delay']
            await asyncio.sleep(rand.randint(minmax[0], minmax[1]))
        else:
            await asyncio.sleep(repconfig['delay'])

def user_generator(users):
    random.shuffle(users)
    c = 0
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
