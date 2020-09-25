import discord
import common
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import command, has_permissions
from discord.ext.commands.errors import CheckFailure
from typing import List
from lib.db import dal

class Control(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="prefix", 
            aliases=[], 
            brief="Set this bot's command prefix",
            help="Sets the command prefixes based on `<prefixes>`, a list of prefixes separated by semi-colons, e.g. `!;??;+;->`")
    @has_permissions(manage_guild=True)
    async def set_prefixes(self, ctx, prefixes):
        filtered = []
        for pref in prefixes.split(common.CSV_SEPARATOR):
            if len(pref) > 5:
                await ctx.send(f"The prefix '{pref}' exceeds the maximum length of 5 charactors.")
            else:
                filtered.append(pref)

        dal.set_prefixes(ctx.guild.id,ctx.guild.name, ctx.author.id, filtered)
        pref_string = ", ".join(filtered)
        await ctx.send(f"Prefixes set to {pref_string}")

    @set_prefixes.error
    async def set_prefixes_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.send("You need Guild Admin permissions to change prefixes.")

    @command(name="leave",
                aliases=[],
                brief="Leave a guild",
                help="Permanently leave the guild with id `[id]`")
    @commands.is_owner()
    async def leave(self, ctx, *, guild_id):
        guild = discord.utils.get(self.bot.guilds, id=guild_id)
        if guild is None:
            await ctx.send("I don't recognize that guild.")
            return
        await self.bot.leave_guild(guild)
        await ctx.send(f":ok_hand: I have left guild: {guild.name} ({guild.id})")

    @command(name="logout",
                aliases=[],
                brief="Log out from Discord",
                help="Log out from Discord")
    @commands.is_owner()
    async def logout(self, ctx):
        self.bot.logout(ctx)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("control")

def setup(bot):
    bot.add_cog(Control(bot))        