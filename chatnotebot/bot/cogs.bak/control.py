import common
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import command, has_permissions
from discord.ext.commands.errors import CheckFailure
from typing import List
from chatnotebot.utils.synchronise import Synchronise

class Control(Cog):
    """Commands to control users and the bot"""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready.booted:
            await Synchronise(self.bot).on_boot()
            self.bot.ready.up(self)        

    # TODO Implement multiple prefixes
    @command(name="prefix", 
            aliases=["prefixes"], 
            brief="Set this bot's command prefix",
            help="Sets the command prefixes based on `<prefixes>`, a list of prefixes separated by semi-colons, e.g. `!;??;+;->`")
    @has_permissions(manage_guild=True)
    async def set_prefixes(self, ctx, prefixes):
        if not prefixes:
            prefix = await self.bot.prefix(ctx.guild)
            await ctx.send(
                f"{self.bot.info} {common.BOT_NAME} prefix in this server is {prefix}. To change it, use `{prefix}config system prefix <new prefix>`."
            )
        else:
            filtered = []
            for pref in prefixes.split(common.CSV_SEPARATOR):
                if len(pref) > 5:
                    await ctx.send(f"The prefix '{pref}' exceeds the maximum length of 5 charactors.")
                else:
                    filtered.append(pref)

            self.bot.db.set_prefixes(ctx.guild.id,ctx.guild.name, ctx.author.id, filtered)
            pref_string = ", ".join(filtered)
            await ctx.send(f"Prefixes set to {pref_string}")

    @set_prefixes.error
    async def set_prefixes_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.send("You need Guild Admin permissions to change prefixes.")

    @command(name="logout",
                aliases=[],
                brief="Log out from Discord",
                help="Log out from Discord")
    @commands.is_owner()
    async def logout(self, ctx):
        self.bot.logout(ctx)


def setup(bot):
    bot.add_cog(Control(bot))        