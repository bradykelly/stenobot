import dal
import common
import dal
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
        name="prefix",
        category="ChatNote"
    )
    async def set_prefix(self, ctx, prefix):
        '''
        Sets the command prefix for this bot
        '''     
        dal.set_prefix(prefix.strip())
      