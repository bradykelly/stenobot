import os
import common
from notes_cog import NoteCommands
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="##", case_insensitive=True, name=common.BOT_NAME, description="Your note taking bot")

bot.add_cog(NoteCommands(bot))
bot.help_command.cog = bot.cogs["NoteCommands"]

bot.run(DISCORD_TOKEN)

