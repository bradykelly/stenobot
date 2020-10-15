# From Solaris: https://github.com/parafoxia/Solaris/blob/master/solaris/utils/__init__.py

import discord
from stenobot import Bot, __version__
intents = discord.Intents(guilds=True, members=True, invites=True, presences=True, messages=True, reactions=True)


def main():
    bot = Bot(__version__, intents=intents)
    bot.run()

if __name__ == "__main__":
    main()
