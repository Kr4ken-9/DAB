import config
import bot


@bot.client.event
async def on_message(message):
    if message.author.id != bot.client.user.id and message.author.id not in bot._config['owners']:
        return

    if message.author.id != bot.client.user.id and message.content.startswith('|'):
        await bot.client.send_message(message.channel, message.content[1:])
        return

    if message.content.startswith('_add'):
        bot._config['channels'].append(message.channel.id)

    if message.content.startswith('_remove'):
        bot._config['channels'].remove(message.channel.id)

    if message.content.startswith('_setrep'):
        bot.repconfig['channel'] = message.channel.id

    if message.content.startswith('_addrep'):
        if type(bot.repconfig['recipients']) is list:
            bot.repconfig['recipients'].append(message.mentions.first().id)
        else:
            recipient = bot.repconfig['recipients']
            bot.repconfig['recipients'] = [recipient, message.mentions.first().id]

    if message.content.startswith('_removerep'):
        if type(bot.repconfig['recipients']) is list:
            bot.repconfig['recipients'].remove(message.mentions.first().id)
        else:
            bot.repconfig['recipients'] = False

    if message.content.startswith('_save'):
        config.save_config('config.yaml', bot._config)
        config.save_config('repconfig.yaml', bot.repconfig)