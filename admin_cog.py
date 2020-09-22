import dal
import common
import dal
from discord.ext.commands.cog import Cog
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from chatnote_cog import ChatNoteCommands

class NoteCommands(ChatNoteCommands, name="Admin"):
    '''
    Cog for various admin commands
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Set the command prefix for the current guild",
        brief="Set command prefix",
        name="prefix",
        aliases=["pref", "prefixes"]
    )
    async def set_prefix(self, ctx, prefixes):
        '''
        Sets the command prefixes for this bot
        '''     
        dal.set_prefixes(ctx.guild.id, prefixes)

    @set_prefix.error
    async def del_book_handler(self, ctx, error):
        '''
        Error handler for the 'del' command
        '''
        if isinstance(error, MissingRequiredArgument):
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")        
      