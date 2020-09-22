from full_embed_help import EmbedHelpCommand
from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands import cog
from discord.utils import get
from chatnote_cog import ChatNoteCommands
"""This custom help command is a perfect replacement for the default one on any Discord Bot written in Discord.py!
However, you must put "bot.remove_command("help")" in your bot, and the command must be in a cog for it to work.

"""
class HelpCommands(ChatNoteCommands, name="Help"):
    """
    Cog for a custom help command
    """
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    def syntax(command):
        cmd_and_aliases = "|".join([str(command), *command.aliases])
        params = []

        for key, value in command.params.items():
            if key not in ["self", "ctx"]:
                params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")
        params = " ".join(params)
        return f"```{cmd_and_aliases} {params}```"


    async def cmd_help(self, ctx, command):
        embed = EmbedHelpCommand(
            title=str(command), 
            #description=syntax(command), 
            color=ctx.author.color)
        embed.add_field(name="Command Description", value=command.help)
        await ctx.send(embed=embed)

    @commands.command(name="help")
    async def show_help(self, ctx, cmd: Optional[str]):
        # From: https://www.youtube.com/watch?v=OrFQzLEGtvc
        '''Shows this message'''
        if cmd is None:
            pass
        else:
            if cmd == get(self.bot.commands, name=cmd):
                await self.cmd_help(ctx, cmd)
            else:
                await ctx.send(f"'{cmd}' does not exist")
    
    @cog.listener()
    async def on_ready(self):
        if not self.bot.ready():
            self.bot.cogs_ready.ready_up("help")
        
    @commands.command(pass_context=True)
    @commands.has_permissions(add_reactions=True,embed_links=True)
    async def dont_help(self,ctx,*cog):
        # Written by Jared Newsom (AKA Jared M.F.)!
        """Gets all cogs and commands of mine."""
        try:
            if not cog:
                """Cog listing.  What more?"""
                halp=discord.Embed(title="Cog Listing and Uncatergorized Commands",
                                description="Use `!help *cog*` to find out more about them!\n(BTW, the Cog Name Must Be in Title Case, Just Like this Sentence.)")
                cogs_desc = ""
                for x in self.bot.cogs:
                    cogs_desc += ("{} - {}".format(x,self.bot.cogs[x].__doc__)+"\n")
                halp.add_field(name="Cogs",value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                cmds_desc = ""
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ("{} - {}".format(y.name,y.help)+"\n")
                halp.add_field(name="Uncatergorized Commands",value=cmds_desc[0:len(cmds_desc)-1],inline=False)
                await ctx.message.add_reaction(emoji="✉")
                await ctx.message.author.send("",embed=halp)
            else:
                """Helps me remind you if you pass too many args."""
                if len(cog) > 1:
                    halp = discord.Embed(title="Error!",description="That is way too many cogs!",color=discord.Color.red())
                    await ctx.message.author.send("",embed=halp)
                else:
                    """Command listing within a cog."""
                    found = False
                    for x in self.bot.cogs:
                        for y in cog:
                            if x == y:
                                halp=discord.Embed(title=cog[0]+" Command Listing",description=self.bot.cogs[cog[0]].__doc__)
                                for c in self.bot.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name,value=c.help,inline=False)
                                found = True
                    if not found:
                        """Reminds you if that cog doesn"t exist."""
                        halp = discord.Embed(title="Error!",description="How do you even use '"+cog[0]+"'?",color=discord.Color.red())
                    else:
                        await ctx.message.add_reaction(emoji="✉")
                    await ctx.message.author.send("",embed=halp)
        except Exception as ex:
            await ctx.send("Excuse me, I can't send help embeds: " + ex.message)
        
    async def help(self, ctx):
        embed = discord.Embed(color=discord.Color.blurple,
        title="ChatNoteBot Help",
        description="Your note taking bot")

        embed.setauthor(name=self.bot.name)

def setup(bot):
    bot.add_command(help)