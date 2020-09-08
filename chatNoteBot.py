import discord
import os
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import bot_has_any_role
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="##", case_insensitive=True, name="ChatNoteBot")

class ChatNoteCommands(Cog, name="ChatNote"):
    @commands.command(
        help="Adds a new note to your current notebook, or the specified notebook",
        brief="Adds a note to a notebook"
    )
    async def note(self, ctx, *, text):
        note_text = text.strip()
        await ctx.channel.send("Noted: " + note_text)

@bot.event
async def on_ready():
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1

    print(f"{bot.user} has connected to Discord! In " + str(guild_count) + " guilds.")    

# bot.remove_command("help")
bot.add_cog(ChatNoteCommands())
bot.help_command.cog = bot.cogs["ChatNote"]

bot.run(DISCORD_TOKEN)

