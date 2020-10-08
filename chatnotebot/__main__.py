# From Solaris: https://github.com/parafoxia/Solaris/blob/master/solaris/utils/__init__.py

from chatnotebot import Bot, __version__


def main():
    bot = Bot(__version__)
    bot.run()

if __name__ == "__main__":
    main()
