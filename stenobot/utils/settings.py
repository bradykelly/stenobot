from stenobot import bot
from stenobot.db import db

class Settings():
    def __init__(self, bot):
        self.db = db.Database(bot)

    async def get_hasrun_runfts(self, guildId):
        hasRun = self.db.field("SELECT runFts FROM guild_config WHERE GuildID = ?", guildId)
        return hasRun

    async def set_hasrun_runfts(self, guildId):
        if await self.db.field("SELECT runFts FROM guild_config WHERE GuildID = ?", guildId) is None:
            await self.db.execute("INSERT INTO guild_config (guildId, runFts) VALUES (?, ?)", guildId, 1)
        else:
            await self.db.execute("UPDATE guild_config SET runFts = 1 WHERE GuildID = ?", guildId)
