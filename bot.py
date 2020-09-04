import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="##")

@bot.command()
async def note(ctx, text):
    note_text = text.strip()
    await ctx.channel.send("Noted: " + note_text)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith("$Hello"):
#         await message.channel.send("Hello")
        
bot.run(DISCORD_TOKEN)

