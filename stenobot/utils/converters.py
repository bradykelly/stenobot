# From Solaris: https://github.com/parafoxia/Solaris

from discord.ext import commands


class User(commands.Converter):
    async def convert(self, ctx, arg):
        if (user := await ctx.bot.grab_user(arg)) is None:
            raise commands.BadArgument
        return user


class Channel(commands.Converter):
    async def convert(self, ctx, arg):
        if (channel := await ctx.bot.grab_channel(arg)) is None:
            raise commands.BadArgument
        return channel


class Guild(commands.Converter):
    async def convert(self, ctx, arg):
        if (guild := await ctx.bot.grab_guild(arg)) is None:
            raise commands.BadArgument
        return guild


class Command(commands.Converter):
    async def convert(self, ctx, arg):
        if (c := ctx.bot.get_command(arg)) is not None:
            return c
        else:
            # Check for subcommands.
            for cmd in ctx.bot.walk_commands():
                if arg == f"{cmd.parent.name} {cmd.name}":
                    return cmd
        raise commands.BadArgument

