from sqlite3.dbapi2 import Row
import common
from lib.bot import bot
from lib.cogs import Welcome
from jishaku import cog

from lib.db import dal
# channel_name = dal.field("select notification_channel from guild_config where guildId = ?", 734386829587120268)
# try:
#     print("None" if channel_name is None else channel_name)
# except Exception as ex:
#     print(str(ex))

def get_notification_channelId(guildId):
    channelName = dal.field("""select notification_channel
                        from guild_config
                        where guildId = ?""", guildId)
    channelId = dal.field("""select channelId from channelIds
                            where guildId = ?
                                and name = ?""", guildId, channelName)
    return channelId  

#chid = get_notification_channelId(734386829587120268)  

bot.run(common.BOT_VERSION)

