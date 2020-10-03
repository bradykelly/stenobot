from lib import bot
from discord.errors import Forbidden
from discord.ext.commands import Cog
from lib.db import dal
import common

class Welcome(Cog):
    """Listeners for when a member joins or leaves the guild"""
    
    def __init__(self, bot):
        self.bot = bot

    def get_notification_channel(self, guildId):
        channelName = dal.field("""select notification_channel
                            from guild_config
                            where guildId = ?""", guildId)
        channelId = dal.field("""select channelId from channelIds
                                where guildId = ?
                                    and name = ?""", guildId, channelName)
        return self.bot.get_channel(channelId)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member): 
        dal.execute("INSERT INTO exp(userId) VALUES (?) ON CONFLICT DO NOTHING", member.id)       
        if chan := self.get_notification_channel(member.guild.id):
            if member.guild.id != common.PY_GUILD_ID:
                await chan.send(f"Welcome to ** {member.guild.name} ** {member.display_name}! Head over to {'Introductions'} and make yourself known.")
            else:
                altChan = self.bot.get_channel(759163418799505409)
                altChan.send(f"Welcome to ** {member.guild.name} ** {member.display_name}! Head over to {'Introductions'} and make yourself known.")
        try:
            #TODO Check which guild I'm in.
            #await member.send(f"Welcome to ** {member.guild.name} **! Enjoy your stay!")
            pass
        except Forbidden:
            raise #LOG

    @Cog.listener()
    async def on_member_remove(self, member):
        dal.execute("DELETE FROM exp WHERE userId = ?", member.id)
        if chan := self.get_notification_channel(member.guild.id):
            if member.guild.id != common.PY_GUILD_ID:
                await chan.send(f"{member.display_name} has left {member.guild.name}")
            else:
                altChan = self.bot.get_channel(759163418799505409)
                altChan.send(f"{member.display_name} has left {member.guild.name}")
def setup(bot):
    bot.add_cog(Welcome(bot))