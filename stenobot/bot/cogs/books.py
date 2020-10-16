import common
import discord
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from stenobot.bot.stenobot_cogs import StenobotBaseCog
from stenobot.utils.stenobot import Stenobot

#TODO Show embeds for exceptions
BOOKS_COMMANDS = ["list", "open", "del"]

class Books(StenobotBaseCog, name="book"):
    """Commands to manage your Stenobot notebooks"""

    def __init__(self, bot):
        self.bot = bot
        self.stenobot = Stenobot(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready.booted:
            self.bot.ready.up(self)      

    @commands.group(
        name="books",
        aliases = ["book", "notebook", "notebooks"],
        title="Commands to help you manage your Stenobot notebooks",
        help="List or delete notebooks.",
        brief="Manage your notebooks",
        usage= f"[list | del]"
    )
    async def books(self, ctx):
        if ctx.invoked_subcommand is None or (ctx.invoked_subcommand is not None and ctx.invoked_subcommand.name not in BOOKS_COMMANDS):
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")

    @books.error
    async def books_handler(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")       

    @books.command(
        name="open",
        aliases = ["choose", "set"], 
        help="Gets or sets which notebook is currently in use. The default is Main.",
        brief="[name]"
    )
    async def open_command(self, ctx, name):
        if not isinstance(name, str):
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage") 
        else:
            await self.stenobot.set_open_book(ctx.guild.id, ctx.message.author.id, name.lower().strip())
        await self.show_message_codeblock(ctx, f"Current notebook set to '{name}'")

    @books.command(
        name="list",
        alias=["show", "all"],
        help="List all your notebooks",
        brief="List notebooks"
    )           
    #FIXME Book names must be unique across all guilds. We need guildId in notes as well.
    async def list(self, ctx):          
        books = await self.stenobot.get_books(ctx.message.author.id)
        list_text = ""
        for book in books:   
            list_text += f"{str(book[0]).zfill(6)}:   {book[1]}\n"
        list_text += "\n" + f"{len(books)} notebook(s)"
        await self.show_message_codeblock(ctx, list_text, f"Notebooks")

    @list.error
    async def list_handler(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")

    @books.command(
        name="del",
        aliases=["delete"],        
        help="Delete a notebook. i.e. Delete all notes in the notebook",
        brief="Delete a notebook",
        usage="<name>: Name of the notebook to delete"
    )
    async def del_book(self, ctx, name):
        count = await self.stenobot.del_book(ctx.message.author.id, name)
        if count > 0:
            await self.show_message_codeblock(ctx, f"Notebook '{name}' deleted' ", "Delete Noteboook")
        else:
            await self.show_message_codeblock(ctx, f"Notebook :'{name}' doesn't exist", "Delete Noteboook")

    @del_book.error
    async def del_book_handler(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")          


def setup(bot):
    bot.add_cog(Books(bot))            