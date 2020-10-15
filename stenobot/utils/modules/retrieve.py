#From Solaris: https://github.com/parafoxia/Solaris/blob/master/solaris/utils/modules/retrieve.py

import discord
import common


async def _system__runfts(bot, guild):
    return await bot.db.field("SELECT runFts FROM guild_config WHERE guildId = ?", guild.id)

async def system__prefix(bot, guild):
    return bot.db.get_prefix(guild.id)    

async def system__defaultlogchannel(bot, guild):
    return bot.get_channel(await bot.db.field("SELECT defaultLogChannelId FROM guild_config WHERE guildId = ?", guild.id))    

async def system__logchannel(bot, guild):
    return bot.get_channel(await bot.db.field("SELECT logChannelId FROM guild_config WHERE guildId = ?", guild.id))    

async def log_channel(bot, guild):
    # An alias function.
    return await system__logchannel(bot, guild)    
   




