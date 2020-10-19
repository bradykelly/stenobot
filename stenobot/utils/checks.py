# From Solaris: https://github.com/parafoxia/Solaris

import common
from discord.ext import commands
from stenobot.utils import settings

class CustomCheckFailure(commands.CheckFailure):
    def __init__(self, message):
        self.msg = message


class BotHasNotBooted(CustomCheckFailure):
    def __init__(self):
        super().__init__(f"{common.BOT_NAME} is still booting. Please try again later.")


def bot_has_booted():
    async def predicate(ctx):
        if not ctx.bot.ready.booted:
            raise BotHasNotBooted()
        return True

    return commands.check(predicate)


class ModuleHasNotInitialised(CustomCheckFailure):
    def __init__(self, module):
        super().__init__(f"The {module} module is still initialising. Please try again later.")


def module_has_initialised(module):
    async def predicate(ctx):
        if not getattr(ctx.bot.ready, module):
            raise ModuleHasNotInitialised(module)
        return True

    return commands.check(predicate)


class BotIsNotReady(CustomCheckFailure):
    def __init__(self):
        super().__init__(f"{common.BOT_NAME} is still performing some start-up procedures. Please try again later.")


def bot_is_ready():
    async def predicate(ctx):
        if not ctx.bot.ready.ok:
            raise BotIsNotReady()
        return True

    return commands.check(predicate)


class GuildIsDiscordBotList(CustomCheckFailure):
    def __init__(self):
        super().__init__(
            "In order to prevent unintended disruption, this command can not be run in the Discord Bot List server. If you wish to test module functionality, you will need to do so in another server."
        )


def guild_is_not_discord_bot_list():
    async def predicate(ctx):
        if ctx.guild.id == 264445053596991498:
            raise GuildIsDiscordBotList()
        return True
    return commands.check(predicate)
