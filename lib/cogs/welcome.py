from discord.ext.commands import Cog
from lib.db import dal


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        channelName = dal.field("""select notification_channel
                                    from guild_config
                                    where guildId = ?""", member.guild.id)
        channelId = dal.field("""select channelId from channelIds
                                where guildId = ?
                                    and name =?""", member.guild.id, channelName)
        pass

    @Cog.listener()
    async def on_member_leave(self, member):
        pass

def setup(bot):
    bot.add_cog(Welcome(bot))