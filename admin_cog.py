import dal
import common
from discord.ext.commands.cog import Cog
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from chatnote_cog import ChatNoteCommands

class NoteCommands(ChatNoteCommands, name="ChatNote Commands"):
    '''
    Cog for admin commands
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Set the command prefix for this bot",
        brief="Set command prefix",
        name="prefix"
    )
    async def set_prefix(self, ctx, prefix):
        '''
        Sets the command prefix for this bot
        '''     
        with open("about.txt", "r") as f:
            about = f.read()
            if about is not None:
                about = about.strip()
            else:
                about = "No help text was found on file"
            await self.show_message_codeblock(ctx, about, f"About {common.BOT_NAME}")        