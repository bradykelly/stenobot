import discord
import os
import sys
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import bot_has_any_role
from discord.ext.commands.errors import MissingRequiredArgument
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
BOT_NAME = "ChatNoteBot"
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
note_args = ["add", "find", "list", "del"]

bot = commands.Bot(command_prefix="##", case_insensitive=True, name=BOT_NAME)

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

        # Greet on each available channel.
        text_channel_list = []
        for guild in self.bot.guilds:
            for channel in guild.channels:
                if (channel.type == "Text"):
                    text_channel_list.append(channel)

        for channel in text_channel_list:
            await channel.send(f"{self.bot.user} is ready and waiting.")     

    @commands.group(
        help="Commands to help you manage your ChatNote notebook",
        brief="Manage your notebook"
    )
    async def note(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("First layer")

    @note.command(
        help="Add some text to your current notebook",
        brief="<text to add>"
    )
    async def add(self, ctx, text):
        note_text = text.strip() 
        await ctx.channel.send(r"add \"" + note_text + "\"")

    @add.error
    async def add_handler(self, ctx, error):
        if isinstance(error, MissingRequiredArgument) and error.param.name == "text":
            await ctx.send_help("add")


bot.add_cog(ChatNoteCommands(bot))
# Include the default help command in our basic cog so the 'help' command doesn't get its own category.
bot.help_command.cog = bot.cogs["ChatNote"]

bot.run(DISCORD_TOKEN)

