import dal
import common
from discord.ext.commands.cog import Cog
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from chatnote_cog import ChatNoteCommands

NOTE_COMMANDS = ["add", "list", "del", "find"]

class NotesCommands(ChatNoteCommands, name="Notes Commands"):
    '''
    Cog for the 'note' command and subcommands
    '''
    def __init__(self, bot):
        self.bot = bot
    
    # 'note' command    
    @commands.group(
        help="Commands to help you manage your ChatNote notebook",
        brief="Use your notebook",
        usage= f"[add | find | list | del] [text]: Default is 'add'. For add, 'text' is required"
    )
    async def note(self, ctx):
        '''
        The root command for the Note group i.e. 'note'
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
        help="Add <text-to-add> to your current notebook, or a named notebook",
        brief="Add text to a notebook",
        usage="<text-to-add> [notebook-name]: Name of a notebook to add a note to. Default is 'Main'"
    )
    async def add(self, ctx, text, notebook=None):
        '''
        Writes a note to a notebook
        '''
        if (notebook is not None):
            notebook = notebook.strip()        
        dal.insert_note(ctx.message.author.id, text, notebook) 
        await self.show_message_codeblock(ctx, r"note added: " + text)

    @add.error
    async def add_handler(self, ctx, error):
        '''
        Error handler for the 'add' command
        '''
        if isinstance(error, MissingRequiredArgument) and error.param.name == "text":
            await self.show_message_codeblock(ctx, self.format_usage(ctx), "Usage")
            
    # 'list' command
    @note.command(
        help="List all notes in your current notebook, or a named notebook",
        brief="List all notes",
        usage="[notebook-name]: Notebook-name (optional) must be a single word"
    )
    async def list(self, ctx, notebook=None):
        '''
        Lists all notes in the default notebook or a named notebook
        '''
        if (notebook is None):
            notebook = common.DEFAULT_NOTEBOOK
        notebook = notebook.strip() 
        notes = dal.get_notes(ctx.message.author.id, notebook)
        note_count = 0
        list_text = ""
        for note in notes:   
            msg = f"{str(note.id).zfill(6)}:   {note.time[:19]}   {note.text}"
            list_text += msg + "\n"
            note_count += 1
        list_text += "\n" + f"{note_count} note(s) in '{notebook}'"
        await self.show_message_codeblock(ctx, list_text, f"Notes in {notebook}")

    # 'del' command
    @note.command(
        help="Delete a note from your notebooks",
        brief="Delete note",
        usage="<note_id>: Id of the note to delete. Required",
        name="del"
    )
    async def delnote(self, ctx, note_id):
        '''
        Deletes a note, by note_id, from the notebook it is in
        '''
        del_id = int(note_id)
        dal.delete_note(ctx.author.id, del_id)
        await self.show_message_codeblock(ctx, f"Note #{del_id} deleted")

    @delnote.error
    async def delnote_handler(self, ctx, error):
        '''
        Error hanlder for the 'delnote' command
        '''
        if isinstance(error, MissingRequiredArgument) and error.param.name == "note_id":
            usage = f"{self.bot.command_prefix}note {ctx.command.name} <note_id>"
            await self.show_message_codeblock(ctx, usage, "Usage")
           
    # 'leave' command
    @commands.command(
        hidden=True
    )
    async def leave(self, ctx):
        server = ctx.message.server
        channel = ctx.message.author.channel
        await channel.leave()

    @Cog.listener()
    async def on_guild_remove(self, guild):
        print(f"{self.bot.user.name} was removed from guild {guild.name}")