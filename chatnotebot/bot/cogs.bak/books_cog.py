import common
from lib.db import dal
from discord.ext.commands.cog import Cog
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from cogs.chatnote_cog import ChatNoteCommands

BOOKS_COMMANDS = ["list", "rename", "del"]

class BooksCommands(ChatNoteCommands, name="Notebook"):
    '''
    Cog for the 'book' command group
    '''
    def __init__(self, bot):
        self.bot = bot
    
    # 'books' command group
    @commands.group(
        title="Commands to help you manage your ChatNote notebooks",
        help="Default is 'list'. For 'del', 'name' is required. For rename, 'name' and 'new-name' are required",
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

    # 'del' command
    @books.command(
        help="Delete a notebook. I.e. Delete all notes in the notebook",
        brief="Delete a notebook",
        usage="<name>: Name of the notebook to delete",
        name="del",
        aliases=["delete"]
    )
    async def del_book(self, ctx, name):
        '''
        Deletes a notebook
        '''
        count = dal.del_book(ctx.message.author.id, name)

        if count > 0:
            await self.show_message_codeblock(ctx, f"Notebook '{name}' deleted' ", "Delete Noteboook")
        else:
            await self.show_message_codeblock(ctx, f"Notebook :'{name}' doesn't exist", "Delete Noteboook")

    @del_book.error
    async def del_book_handler(self, ctx, error):
        '''
        Error handler for the 'del' command
        '''
        if isinstance(error, MissingRequiredArgument):
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")