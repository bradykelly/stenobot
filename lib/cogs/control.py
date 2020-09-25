import discord
from discord.ext import commands
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import command


class Control(Cog):
    def __init__(self, bot):
        self.bot = bot

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