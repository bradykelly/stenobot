import os
import common
import dal
from full_embed_help import EmbedHelpCommand
from small_embed_help import MyNewHelp
from help_cog import HelpCommands
from notes_cog import NotesCommands
from misc_cog import MiscCommands
from dotenv import load_dotenv
from discord.ext import commands
from books_cog import BooksCommands
from notes_cog import NotesCommands
from misc_cog import MiscCommands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

async def _prefix_callable(bot, message):
    """ 
    Determines the list of command prefixes for the current guild
    """
    if message.guild:
        prefList = dal.get_prefixes(message.guild.id)
        if prefList is None:
            prefList = common.DEFAULT_PREFIXES
        else:
            prefList.extend(prefList.split(";"))
    else:
        prefList = common.DEFAULT_PREFIXES
    print("callable", prefList, message.content)
    return prefList

bot = commands.Bot(command_prefix=_prefix_callable, name=common.BOT_NAME, description=f"{common.BOT_NAME}. Your note taking bot.")

@bot.event
async def on_message(message):
    print("on_message", message.content)
    if message.author.bot:
        return
    await bot.process_commands(message)

bot.add_cog(NotesCommands(bot))
bot.add_cog(BooksCommands(bot))
bot.add_cog(MiscCommands(bot))
bot.add_cog(HelpCommands(bot))
print(f"Cogs: {len(bot.cogs)}")
bot.help_command.cog = bot.cogs["Help"]
#bot.help_command = embed_help.MyNewHelp()
#bot.help_command=EmbedHelpCommand()

bot.run(DISCORD_TOKEN)

