import backend
from discord.ext.commands.cog import Cog
from discord.ext.commands.errors import MissingRequiredArgument
from discord.ext import commands

class ChatNoteCommands(Cog, name="ChatNoteCommands"):
    
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):

        # List guilds this bot is connected to.
        guild_count = 0
        for guild in self.bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")
            guild_count += 1
        print(f"{self.bot.user} has connected to Discord! In " + str(guild_count) + " guilds.")  

    # 'note' command group
    @commands.group(
        help="Commands to help you manage your ChatNote notebook",
        brief="Manage your notebook",
        usage=f"[add | find | list | del] [text]: Default is 'add'. For add, 'text' is required"
    )
    async def note(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("First layer")

    # Add command
    @note.command(
        help="Adds <text-to-add> to your current notebook, or a named notebook",
        brief="Add text to a notebook",
        usage="[notebook-name] <text-to-add>: Notebook-name (optional) must be a single word"
    )
    async def add(self, ctx,  notebook=None, *, text=None):
        if (notebook is not None):
            notebook = notebook.strip()        
        if text is not None:
            text = text.strip() 
        backend.insert_note(ctx.message.author.id, text, notebook) 
        await ctx.channel.send(r"note added: " + text)

    @add.error
    async def add_handler(self, ctx, error):
        if isinstance(error, MissingRequiredArgument) and error.param.name == "text":
            await ctx.channel.send(f"Usage: {bot.command_prefix}note add <text-to-add>")

    # List command
    @note.command(
        help="Lists all notes in yoour current notebook, or a named notebook",
        brief="Lists all notes",
        usage="[notebook-name]: Notebook-name (optional) must be a single word"
    )
    async def list(self, ctx, notebook=None):
        if (notebook is None):
            notebook = backend.DEFAULT_NOTEBOOK
        notebook = notebook.strip() 
        notes = backend.get_notes(ctx.message.author.id, notebook)
        note_count = 0
        for note in notes:            
            await ctx.channel.send(f"{str(note.id).zfill(6)}:   {note.time[:19]}   {note.text}")
            note_count += 1
        await ctx.channel.send(f"{note_count} note(s) in '{notebook}'")

    # leave command
    @commands.command(hidden=True)
    async def leave(self, ctx):
        server = ctx.message.server
        channel = ctx.message.author.channel
        await channel.leave()
