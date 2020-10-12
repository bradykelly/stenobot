# From Solaris: https://github.com/parafoxia/Solaris

import common
from discord.ext import commands


class System(commands.Cog):
    """System attributes."""

    def __init__(self, bot):
        self.bot = bot
        self.configurable = True

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready.booted:
            self.bot.ready.up(self)

    @commands.command(
        name="prefix", help=f"Displays {common.BOT_NAME}' prefix in your server. Note that mentioning {common.BOT_NAME} will always work."
    )
    async def prefix_command(self, ctx):
        prefix = await self.bot.prefix(ctx.guild)
        await ctx.send(
            f"{self.bot.info} {common.BOT_NAME}' prefix in this server is {prefix}. To change it, use `{prefix}config system prefix <new prefix>`."
        )


def setup(bot):
    bot.add_cog(System(bot))
