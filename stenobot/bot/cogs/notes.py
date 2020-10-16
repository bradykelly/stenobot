import common
import discord
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from stenobot.bot.stenobot_cogs import StenobotBaseCog
from stenobot.utils.stenobot import Stenobot

NOTE_COMMANDS = ["add", "list", "del", "find"]

class Notes(StenobotBaseCog, name="note"):
    """Commands to use your Stenobot notes"""

    def __init__(self, bot):
        self.bot = bot
        self.stenobot = Stenobot(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready.booted:
            self.bot.ready.up(self)          
    
    # 'note' command group
    @commands.group(
        aliases=["notes"],
        title="Commands to help you manage your Stenobot notes",
        help=f"Add, list or delete notes",
        brief="Use your notebook",
        usage= f"add <note-text> \nnote list \nnote del <note-number>]"
    )
    async def note(self, ctx):
        '''
        The root command for the Note command group i.e. 'note'
        '''
        if ctx.invoked_subcommand is None or (ctx.invoked_subcommand is not None and ctx.invoked_subcommand.name not in NOTE_COMMANDS):
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")

    @note.error
    async def note_handler(self, ctx, error):
        '''
        Error handler for all commands in the 'note' group
        '''
        if isinstance(error, CommandNotFound):
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")

    # 'add' command
    @note.command(
        name="add",
        help="Add <text-to-add> to your current notebook",
        brief="Add a note",
        description="<text-to-add>"
    )
    async def add_command(self, ctx, *, text):
        await self.stenobot.insert_note(ctx.guild.id, ctx.message.author.id, text)
        await self.show_message_codeblock(ctx, r"Note added: " + text)

    @add_command.error
    async def add_handler(self, ctx, error):
        if isinstance(error, MissingRequiredArgument) and error.param.name == "text":
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")
            
    @note.command(
        name="list",
        help="List all notes in your current notebook, or a named notebook",
        brief="List all notes",
        usage="[notebook-name]: Notebook-name (optional) must be a single word"
    )
    async def list_command(self, ctx, notebook=None):
        notes, notebook = await self.stenobot.get_notes(ctx.guild.id, ctx.message.author.id, notebook)
        list_text = ""
        for note in notes:   
            list_text += f"{str(note.id).zfill(6)}:   {note.time[:19]}   {note.text}\n"
        list_text += "\n" + f"{len(notes)} note(s) in '{notebook}'"
        await self.show_message_codeblock(ctx, list_text, f"Notes in {notebook}")

    @note.command(
        name="del",
        aliases=["delete"],
        help="Delete a note from your notebooks",
        brief="Delete a note",
        usage="<note_id>: Id of the note to delete. Required"
    )
    async def del_command(self, ctx, note_id):
        await self.stenobot.delete_note(ctx.message.author.id, int(note_id))
        await self.show_message_codeblock(ctx, f"Note #{note_id} deleted")

    @del_command.error
    async def delnote_handler(self, ctx, error):
        if isinstance(error, MissingRequiredArgument) and error.param.name == "note_id":
            usage = f"{ctx.prefix}{ctx.command.name} <note_id>"
            await self.show_message_codeblock(ctx, usage, "Usage")     


def setup(bot):
    bot.add_cog(Notes(bot))  