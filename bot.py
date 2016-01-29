from discord.ext import commands
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
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


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    def __repr__(self):
        return "<Message(id='%s', timestamp='%s', content='%s', author_id='%s')>" % (
            self.id, self.timestamp, self.content, self.user_id)


engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)


def main():
    config = configparser.ConfigParser()
    config.read('discord-stats.conf')

    email = config['DEFAULT']['User']
    password = config['DEFAULT']['Password']
    bot.run(email, password)


if __name__ == '__main__':
    main()
