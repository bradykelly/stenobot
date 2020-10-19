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


class FirstTimeSetupNotRun(CustomCheckFailure):
    def __init__(self, prefix=">>", /):
        super().__init__(
            f"The first time setup needs to be run before you can do that. Use `{prefix}setup` to do this."
        )


def first_time_setup_has_run():
    async def predicate(ctx):
        if not await settings.get_hasrun_runfts(ctx.guild.id):
            raise FirstTimeSetupNotRun(await ctx.bot.prefix(ctx.guild))
        return True
    return commands.check(predicate)


class FirstTimeSetupRun(CustomCheckFailure):
    def __init__(self):
        super().__init__("The first time setup has already been run.")


def first_time_setup_has_not_run():
    async def predicate(ctx):
        if await settings.get_hasrun_runfts(ctx.guild.id):
            raise FirstTimeSetupRun()
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
