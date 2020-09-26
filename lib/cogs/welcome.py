from discord.errors import Forbidden
from discord.ext.commands import Cog
from lib.db import dal


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_notification_channelId(self, guildId):
        channelName = dal.field("""select notification_channel
                            from guild_config
                            where guildId = ?""", guildId)
        channelId = dal.field("""select channelId from channelIds
                                where guildId = ?
                                    and name = ?""", guildId, channelName)
        return channelId

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member): 
        dal.execute("INSERT INTO epx(userId) VALUES (?)", member.id)       
        channelId = self.get_notification_channelId(member.guild.id)
        #TODO Get intro channel id from db
        await self.bot.get_channel(channelId).send(f"Welcome to ** {member.guild.name} ** {member.mention}! \
            Head over to {'Introductions'} and make yourself known.")

        try:
            await member.send(f"Welcome to ** {member.guild.name} **! Enjoy your stay!")
        except Forbidden:
            raise #LOG

    @Cog.listener()
    async def on_member_leave(self, member):
        pass

def setup(bot):
    bot.add_cog(Welcome(bot))