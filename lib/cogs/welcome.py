from discord.ext.commands import Cog
from discord.ext.commands import Commands


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        pass

    @Cog.listener()
    async def on_member_leave(self, member):
        pass

def setup(bot):
    bot.add_cog(Welcome(bot))