import discord
from common import BOT_NAME
import dal
import common
from datetime import datetime
from discord.ext.commands.cog import Cog
from discord.ext.commands.errors import MissingRequiredArgument
from discord.ext import commands

class NoteCommands(Cog, name="NoteCommands"):
    
    def __init__(self, bot):
        self.bot = bot
    
    def get_guild_count(self):
        guild_count = 0
        for guild in self.bot.guilds:
            guild_count += 1
        return guild_count

    async def show_message_embed(self, ctx: commands.Context, message, title=None):
        if title is None:
            title = f"Command Output"
        em = discord.Embed(title=title, description=message, colour=0xBD362F)
        #em.set_footer("ChatNote (c) 2020 Erisia")
        em.timestamp = datetime.utcnow()
        await ctx.send(embed=em)

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} ({self.bot.user.id}) has connected to Discord! In " + str(self.get_guild_count()) + " guild(s).")  

    # 'note' command
    @commands.group(
        help="Commands to help you manage your ChatNote notebook",
        brief="Use your notebook",
        usage=f"[add | find | list | del] [text]: Default is 'add'. For add, 'text' is required"
    )
    async def note(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("First layer")

    # 'add command
    @note.command(
        help="Add <text-to-add> to your current notebook, or a named notebook",
        brief="Add text to a notebook",
        usage="[notebook-name] <text-to-add>: Notebook-name (optional) must be a single word"
    )
    async def add(self, ctx, text, notebook=None):
        if (notebook is not None):
            notebook = notebook.strip()        
        dal.insert_note(ctx.message.author.id, text, notebook) 
        await self.show_message_embed(ctx, r"note added: " + text)

    @add.error
    async def add_handler(self, ctx, error):
        if isinstance(error, MissingRequiredArgument) and error.param.name == "text":
            await self.show_message_embed(ctx, f"{self.bot.command_prefix}note add <text-to-add>", "Usage")

    # 'list' command
    @note.command(
        help="List all notes in your current notebook, or a named notebook",
        brief="List all notes",
        usage="[notebook-name]: Notebook-name (optional) must be a single word"
    )
    async def list(self, ctx, notebook=None):
        if (notebook is None):
            notebook = common.DEFAULT_NOTEBOOK
        notebook = notebook.strip() 
        notes = dal.get_notes(ctx.message.author.id, notebook)
        note_count = 0
        list_text = ""
        for note in notes:   
            msg = f"{str(note.id).zfill(6)}:   {note.time[:19]}   {note.text}"
            #await ctx.channel.send(msg)
            list_text += msg + "\n"
            note_count += 1
        list_text += "\n" + f"{note_count} note(s) in '{notebook}'"
        await self.show_message_embed(ctx, list_text, f"Notes in {notebook}")

    # 'del' command
    @note.command(
        help="Delete a note from your notebooks",
        brief="Delete note",
        usage="<note_id>: Id of the note to delete. Required",
        name="del"
    )
    async def delnote(self, ctx, note_id):
        del_id = int(note_id)
        dal.delete_note(ctx.author.id, del_id)
        await self.show_message_embed(ctx, f"Note #{del_id} deleted")

    @delnote.error
    async def delnote_handler(self, ctx, error):
        if isinstance(error, MissingRequiredArgument) and error.param.name == "note_id":
            usage = f"{self.bot.command_prefix}note del <note_id>"
            await self.show_message_embed(ctx, usage, "Usage")

    @commands.command(
        help="Shows the About info for this bot",
        brief="Shows About info",
        name="about"
    )
    async def show_about(self, ctx):
        msg = "No help text was found"        
        with open("about.txt", "r") as f:
            about = f.read()
            if about is not None:
                about = about.strip()
            await self.show_message_embed(ctx, about, f"About {common.BOT_NAME}")
            
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