import dal
import common
from discord.ext.commands.cog import Cog
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from chatnote_cog import ChatNoteCommands

BOOKS_COMMANDS = ["list", "rename", "del"]

class BooksCommands(ChatNoteCommands, name="Notebook Commands"):
    '''
    Cog for the 'note' command and subcommands
    '''
    def __init__(self, bot):
        self.bot = bot
    
    # 'books' command group
    @commands.group(
        help="Commands to help you manage your ChatNote notebooks",
        brief="Manage your notebooks",
        usage= f"[list | rename | del] [name] [new-name]: Default is 'list'. For 'del', 'name' is required. For rename, 'name' and 'new-name' are required"
    )
    async def books(self, ctx):
        '''
        The root command for the Books group
        '''
        if ctx.invoked_subcommand is None or (ctx.invoked_subcommand is not None and ctx.invoked_subcommand.name not in BOOKS_COMMANDS):
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")

    @books.error
    async def books_handler(self, ctx, error):
        '''
        Error handler for all commands in the 'books' group
        '''
        if isinstance(error, CommandNotFound):
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")       

    # 'list' command
    @books.command(
        help="List all your notebooks",
        brief="List notebooks"
    )           
    async def list(self, ctx):          
        '''
        Lists all a user's notebooks
        '''
        books = dal.get_books(ctx.message.author.id)
        book_count = 0
        list_text = ""
        for book in books:   
            msg = f"{str(book[0]).zfill(6)}:   {book[1]}"
            list_text += msg + "\n"
            book_count += 1
        list_text += "\n" + f"{book_count} notebook(s)"
        await self.show_message_codeblock(ctx, list_text, f"Notebooks")

    @list.error
    async def list_handler(self, ctx, error):
        '''
        Error handler for the 'list' command
        '''
        if isinstance(error, MissingRequiredArgument):
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")
            