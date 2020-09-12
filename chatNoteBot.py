from asyncio.base_events import Server
import discord
import os
import sys
import backend
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import bot_has_any_role
from discord.ext.commands.errors import MissingRequiredArgument
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
BOT_NAME = "ChatNoteBot"
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
note_args = ["add", "find", "list", "del"]

bot = commands.Bot(command_prefix="##", case_insensitive=True, name=BOT_NAME, description="A note taking bot")

class ChatNoteCommands(Cog, name="ChatNote"):

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
    async def add(self, ctx,  text):
        note_text = text.strip() 
        # For now we always use the default notebook name, used when None is passed.
        backend.insert_note(ctx.message.author.id, text, None) 
        await ctx.channel.send(r"note added: " + note_text)

    # leave command
    @commands.command(hidden=True)
    async def leave(self, ctx):
        server = ctx.message.server
        channel = ctx.message.author.channel
        await channel.leave()

    @add.error
    async def add_handler(self, ctx, error):
        # TODO Find out why send_help didn't work.
        if isinstance(error, MissingRequiredArgument) and error.param.name == "text":
            await ctx.channel.send(f"Usage: {bot.command_prefix}note add <text-to-add>")


bot.add_cog(ChatNoteCommands(bot))
# Include the default help command in our basic cog so the 'help' command doesn't get its own category.
bot.help_command.cog = bot.cogs["ChatNote"]

bot.run(DISCORD_TOKEN)

