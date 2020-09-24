from aiohttp import request
from typing import Optional
from discord import Member
from random import randint
from discord import embeds
from discord.embeds import Embed
from discord.errors import HTTPException
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands.errors import BadArgument

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}!")

    @command(name="dice", aliases=["roll"])
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))
        if dice <= 25:
            rolls = [randint(1, value) for i in range(dice)]
            await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")
        else:
            await ctx.send("I can't roll that many dice. Please try a lower number.")

    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}")
        
    @slap_member.error
    async def slap_member_error(self, ctx, error):
        if isinstance(error, BadArgument):
            ctx.send("Member not found")

    @command(name="echo", aliases=["say"])
    async def echo_message(self, ctx, *, message: str):
        await ctx.send(f"{ctx.author.display_name}")

    @command(name="fact")
    async def animal_fact(self, ctx, animal: str):
        if animal.lower() in ("dog", "cat", "panda", "fox", "bird", "koala"):
            url = f"https://some-random-api.ml/facts/{animal.lower()}"

            async with request("GET", url, headers=[]) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(title=f"{animal} fact", 
                                    description=data["fact"], 
                                    color=ctx.author.color)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"API returned a {response.status} status.")
        else:
            await ctx.send(f"No facts are available for '{animal}'.'")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Fun")
        print("Fun cog ready")

def setup(bot):
    bot.add_cog(Fun(bot))