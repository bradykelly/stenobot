from discord import embeds
from discord.embeds import Embed
from discord.ext.commands.cog import Cog
from full_embed_help import EmbedHelpCommand
from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands import cog
from discord.utils import get
from cogs.chatnote_cog import ChatNoteCommands

class HelpCommands(ChatNoteCommands, name="Help"):
    """
    Cog for a custom help command
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.remove_command("help")

    def syntax(self, command: commands.Command):
        cmd_and_aliases = "|".join([str(command), *command.aliases])
        params = []

        for key, value in command.params.items():
            if key not in ["self", "ctx"]:
                params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")
        params = " ".join(params)
        return f"```{cmd_and_aliases} {params}```"

    async def cmd_help(self, ctx, command):
        try:
            embed = Embed(
                title="Help with " + str(command), 
                description=self.syntax(command), 
                color=ctx.author.color)
            embed.add_field(name=f"{str(command)}", value=command.usage)
            await ctx.send(embed=embed)
        except Exception as ex:
            print(ex)
        
    @commands.command(
        name="help", 
        help="The Help command",
        usage="help [cmd]. Get help on the specified command")
    @commands.has_permissions(add_reactions=True,embed_links=True)
    async def show_help(self, ctx, cmd=None):
        # From: https://www.youtube.com/watch?v=OrFQzLEGtvc
        '''Shows this message'''
        if cmd is None:
            pass
        else:
            if cmd := get(self.bot.commands, name=cmd):
                await self.cmd_help(ctx, cmd)
            else:
                await ctx.send(f"'{cmd}' does not exist")
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.is_ready():
            self.bot.cogs_ready.ready_up("help")

def setup(bot):
    bot.add_command(help)