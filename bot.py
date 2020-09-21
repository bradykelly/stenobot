import os
import common
from notes_cog import NotesCommands
from misc_cog import MiscCommands
from dotenv import load_dotenv
from discord.ext import commands
from books_cog import BooksCommands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=common.COMMAND_PREFIX, case_insensitive=True, name=common.BOT_NAME, description=f"{common.BOT_NAME}. Your note taking bot")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

bot.add_cog(NotesCommands(bot))
bot.add_cog(BooksCommands(bot))
bot.add_cog(MiscCommands(bot))
bot.help_command.cog = bot.cogs["Notes Commands"]

bot.run(DISCORD_TOKEN)

