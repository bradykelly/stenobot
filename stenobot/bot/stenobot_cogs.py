
import discord
from discord.ext.commands.errors import CommandNotFound
import common
from datetime import datetime
from discord.ext import commands
from discord.ext.commands.cog import Cog

class StenobotBaseCog(Cog):
    '''
    Base class for application cogs in this bot
    '''
    def __init__(self, bot):
        self.bot = bot

    def format_usage(self, ctx):
        '''
        Contructs a formatted usage string for a command.
        '''
        usg = f"{ctx.prefix}{ctx.command.name} {ctx.command.usage}"
        return usg

    async def show_message_embed(self, ctx, message, title=None):
        '''
        Shows the user a message in an embed
        '''
        if title is None:
            title = f"Command Output"
        em = discord.Embed(title=title, description="```\n" + message + "\n```", colour=0xBD362F)
        em.set_footer(text="Stenobot (c) 2020 Erisia")
        em.timestamp = datetime.utcnow()
        await ctx.send(embed=em)

    async def show_message_codeblock(self, ctx, message, title=None):
        '''
        Shows the user a message in the format of a code block
        '''
        msg = "```\n"
        if title is not None:
            msg += title + "\n\n"
        msg += message
        msg += "\n```"
        await ctx.send(msg)




