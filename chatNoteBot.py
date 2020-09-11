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

        # Greet on each available channel.
        text_channel_list = []
        for guild in self.bot.guilds:
            for channel in guild.channels:
                if (channel.type == "Text"):
                    text_channel_list.append(channel)

        for channel in text_channel_list:
            await channel.send(f"{self.bot.user} is ready and waiting.")

        # List guilds this bot is connected to.
        guild_count = 0
        for guild in self.bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")
            guild_count += 1
        print(f"{self.bot.user} has connected to Discord! In " + str(guild_count) + " guilds.")   

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        # Ignore commands with local error handlers.
        if hasattr(ctx.command, "on_error"):
            return

        # Prevent any cogs with an overwritten cog_command_error being handled here
        cog = ctx.cog
        if cog:
            if cog.get_overriden_method(cog.cog_command_error) is not None:
                return

        # Check for original exceptions raised and sent to CommandInvokeError. 
        # If nothing is found we keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        print(f"Ignoring exception in command {ctx.command}", file=sys.stderr)        

    @commands.command(
        help="Adds a new note to your current notebook, or the specified notebook",
        brief="Adds a note to a notebook"
    )
    async def note(self, ctx, action, *, text):
        note_text = text.strip()
        await ctx.channel.send(f"{action}: " + note_text)

    @note.error
    async def note_handler(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            if error.param.name == "action":
                await ctx.send(f"{bot.command_prefix}note [add|find|list|delete] [text]")






bot.add_cog(ChatNoteCommands(bot))
# Include the default help command in our basic cog so the 'help' command doesn't get its own category.
bot.help_command.cog = bot.cogs["ChatNote"]

bot.run(DISCORD_TOKEN)

