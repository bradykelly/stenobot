import discord
import common
from chatnotebot.db import dal
from discord.ext.commands.cog import Cog
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from cogs.chatnote_cog import ChatNoteCommands

class MiscCommands(ChatNoteCommands, name="Misc."):
    '''
    Cog for misc commands and events
    '''
    def get_guilds(self):
        '''
        Gets the guilds this bot is connected to
        '''
        return self.bot.guilds

    @commands.command(
        help="Show the About info for this bot",
        brief="Show About info",
        name="about",
        category="ChatNote"
    )
    async def show_about(self, ctx):
        '''
        Shows the about info for this bot
        '''     
        with open("about.txt", "r") as f:
            about = f.read()
            if about is not None:
                about = about.strip()
            else:
                about = "No About text was found on file"
            await self.show_message_codeblock(ctx, about, f"About {common.BOT_NAME}")

    @Cog.listener()
    async def on_ready(self):
        '''
        Prints details of a new Discord connection
        '''
        await self.bot.change_presence(activity = discord.Activity(
                          type = discord.ActivityType.custom,
                          name = 'Taking notes...'))
        print(f"{self.bot.user} ({self.bot.user.id}) has connected to Discord! In " + str(len(self.get_guilds())) + " guild(s).")

    @Cog.listener()
    async def on_command_error(self, ctx, error)  :
        if isinstance(error, CommandNotFound):
            await ctx.send_help()