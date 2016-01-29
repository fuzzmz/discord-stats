from discord.ext import commands
import configparser


description = '''A helper bot which generates stats.'''
bot = commands.Bot(command_prefix='?', description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def messages(name: str, lim: int):
    """List messages for channel.
    :param lim: limit to last x messages
    :param name: channel name
    """
    counter = 0
    for channel in bot.get_all_channels():
        if channel.name == name:
            chid = channel.id
            await bot.say(channel.name + ' ' + chid)
            async for message in bot.logs_from(channel, limit=lim):
                await bot.say(str(message.timestamp) + ' : ' + message.author.name + ' ' + message.content)
    counter += 1


config = configparser.ConfigParser()
config.read('discord-stats.conf')

email = config['DEFAULT']['User']
password = config['DEFAULT']['Password']
bot.run(email, password)
