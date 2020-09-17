import os
import common
from note_cog import NoteCommands
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=common.COMMAND_PREFIX, case_insensitive=True, name=common.BOT_NAME, description=f"{common.BOT_NAME}. Your note taking bot")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith(">--"):
        return
    await bot.process_commands(message)

bot.add_cog(NoteCommands(bot))
bot.help_command.cog = bot.cogs["ChatNote Commands"]

bot.run(DISCORD_TOKEN)

