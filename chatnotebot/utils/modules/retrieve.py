#From Solaris: https://github.com/parafoxia/Solaris/blob/master/solaris/utils/modules/retrieve.py

import discord
from ....common import common


async def _system__runfts(bot, guild):
    return await bot.db.field("SELECT run_fts FROM guild_config WHERE guildId = ?", guild.id)

async def system__prefix(bot, guild):
    return bot.dal.get_prefix(guild.id)    

async def system__defaultlogchannel(bot, guild):
    return bot.get_channel(await bot.db.field("SELECT default_log_channel_id FROM guild_config WHERE guildId = ?", guild.id))    

async def system__logchannel(bot, guild):
    return bot.get_channel(await bot.db.field("SELECT log_channel_id FROM guild_config WHERE guildId = ?", guild.id))    

async def log_channel(bot, guild):
    # An alias function.
    return await system__logchannel(bot, guild)    

async def system__defaultadminrole(bot, guild):
    return guild.get_role(await bot.db.field("SELECT default_admin_role_id FROM guild_config WHERE guildId = ?", guild.id))

async def system__adminrole(bot, guild):
    return guild.get_role(await bot.db.field("SELECT admin_role_id FROM guild_config WHERE guildId = ?", guild.id))    

async def _gateway__active(bot, guild):
    return bool(await bot.db.field("SELECT active FROM gateway WHERE guildId = ?", guild.id))

async def gateway__ruleschannel(bot, guild):
    return bot.get_channel(await bot.db.field("SELECT rules_channel_id FROM gateway WHERE guildId = ?", guild.id))    

async def _gateway__gatemessage(bot, guild):
    try:
        rc_id, gm_id = await bot.db.record(
            "SELECT rules_channel_id, gate_message_id FROM gateway WHERE guildId = ?", guild.id
        )
        return await bot.get_channel(rc_id).fetch_message(gm_id)
    except discord.NotFound:
        return None    

async def gateway__blockingrole(bot, guild):
    return guild.get_role(await bot.db.field("SELECT blocking_role_id FROM gateway WHERE guildId = ?", guild.id))

async def gateway__memberroles(bot, guild):
    if ids := await bot.db.field("SELECT member_role_ids FROM gateway WHERE guildId = ?", guild.id):
        return [guild.get_role(int(id_)) for id_ in ids.split(common.CSV_SEPARATOR)]
    else:
        return []

async def gateway__exceptionroles(bot, guild):
    if ids := await bot.db.field("SELECT exception_role_ids FROM gateway WHERE guildId = ?", guild.id):
        return [guild.get_role(int(id_)) for id_ in ids.split(",")]
    else:
        return []        

async def gateway__welcomechannel(bot, guild):
    return bot.get_channel(await bot.db.field("SELECT welcome_channel_id FROM gateway WHERE guildId = ?", guild.id))

async def gateway__goodbyechannel(bot, guild):
    return bot.get_channel(await bot.db.field("SELECT goodbye_channel_id FROM gateway WHERE guildId = ?", guild.id))

async def gateway__timeout(bot, guild):
    return await bot.db.field("SELECT timeout FROM gateway WHERE guildId = ?", guild.id)

async def gateway__gatetext(bot, guild):
    return await bot.db.field("SELECT gate_text FROM gateway WHERE guildId = ?", guild.id)

async def gateway__welcometext(bot, guild):
    return await bot.db.field("SELECT welcome_text FROM gateway WHERE guildId = ?", guild.id)

async def gateway__goodbyetext(bot, guild):
    return await bot.db.field("SELECT goodbye_text FROM gateway WHERE guildId = ?", guild.id)

async def gateway__welcomebottext(bot, guild):
    return await bot.db.field("SELECT welcome_bot_text FROM gateway WHERE guildId = ?", guild.id)

async def gateway__goodbyebottext(bot, guild):
    return await bot.db.field("SELECT goodbye_bot_text FROM gateway WHERE guildId = ?", guild.id)

async def warn__warnrole(bot, guild):
    return guild.get_role(await bot.db.field("SELECT warn_role_id FROM warn WHERE guildId = ?", guild.id))

async def warn__maxpoints(bot, guild):
    return await bot.db.field("SELECT max_points FROM warn WHERE guildId = ?", guild.id)

async def warn__maxstrikes(bot, guild):
    return await bot.db.field("SELECT max_strikes FROM warn WHERE guildId = ?", guild.id)
