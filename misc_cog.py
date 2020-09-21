import dal
import common
from discord.ext.commands.cog import Cog
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from chatnote_cog import ChatNoteCommands

class MiscCommands(ChatNoteCommands, name="Misc. Commands"):
    '''
    Cog for misc commands and events
    '''
    def get_guild_count(self):
        '''
        Gets the number of guilds this bot is connected to
        '''
        guild_count = 0
        for guild in self.bot.guilds:
            guild_count += 1
        return guild_count

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
                about = "No help text was found on file"
            await self.show_message_codeblock(ctx, about, f"About {common.BOT_NAME}")

    @Cog.listener()
    async def on_ready(self):
        '''
        Prints details of a new Discord connection
        '''
        print(f"{self.bot.user} ({self.bot.user.id}) has connected to Discord! In " + str(self.get_guild_count()) + " guild(s).")

    @Cog.listener()
    async def on_command_error(self, ctx, error)  :
        if isinstance(error, CommandNotFound):
            await ctx.send_help()