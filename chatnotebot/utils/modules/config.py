# From Solaris: https://github.com/parafoxia/Solaris/blob/master/solaris/utils/modules/config.py

import discord
from os import getenv
from dotenv import load_dotenv
from chatnotebot.utils.modules import retrieve
import common

MAX_PREFIX_LEN = 5

MAX_MEMBER_ROLES = 3
MAX_EXCEPTION_ROLES = 3
MIN_TIMEOUT = 1
MAX_TIMEOUT = 60
MAX_GATETEXT_LEN = 250
MAX_WGTEXT_LEN = 1000
MAX_WGBOTTEXT_LEN = 500

MIN_POINTS = 5
MAX_POINTS = 99
MIN_STRIKES = 1
MAX_STRIKES = 9

async def _system__runfts(bot, channel, value):
    await bot.db.execute("UPDATE guild_config SET runFts = ? WHERE guildId = ?", value, channel.guild.id)

async def system__prefix(bot, channel, value):
    """The server prefix
    The bot's mention responds to, aside from mentions. The default is >-."""
    if not isinstance(value, str):
        await channel.send(f"{bot.cross} A server prefix must be a string.")
    elif len(value) > MAX_PREFIX_LEN:
        await channel.send(
            f"{bot.cross} A server prefix must be no longer than {MAX_PREFIX_LEN} characters in length."
        )
    else:
        await bot.db.execute("UPDATE guild_config SET commandPrefix = ? WHERE guildId = ?", value, channel.guild.id)
        await channel.send(f"{bot.tick} The server prefix has been set to {value}.")
        lc = await retrieve.log_channel(bot, channel.guild)
        await lc.send(f"{bot.info} The server prefix has been set to {value}.")    

async def system__logchannel(bot, channel, value):
    """The log channel
    The channel this bot uses to communicate important information. It is recommended you keep this channel restricted to members of the server's moderation team. Upon selecting a new channel, this bot will delete the one that was created during the first time setup should it still exist."""
    if not isinstance(value, discord.TextChannel):
        await channel.send(f"{bot.cross} The log channel must be a Discord text channel in this server.")
    elif not value.permissions_for(channel.guild.me).send_messages:
        await channel.send(f"{bot.cross} The given channel can not be used as the log channel as {common.BOT_NAME} can not send messages to it.")
    else:
        await bot.db.execute("UPDATE guild_config SET log_channel_id = ? WHERE guildId = ?", value.id, channel.guild.id)
        await channel.send(f"{bot.tick} The log channel has been set to {value.mention}.")
        await value.send(
            (
                f"{bot.info} This is the new log channel. {common.BOT_NAME} will use this channel to communicate with you if needed. "
                "Configuration updates will also be sent here."
            )
        )

        if (
            channel.guild.me.guild_permissions.manage_channels
            and (dlc := await retrieve.system__defaultlogchannel(bot, channel.guild)) is not None
        ):
            await dlc.delete(reason="Default log channel was overridden.")
            await value.send(f"{bot.info} The default log channel has been deleted, as it is no longer required.")        

async def system__adminrole(bot, channel, value):
    """The admin role
    The role used to denote which members can configure this bot. Alongside server administrators, only members with this role can use any of this bot's configuration commands. Upon selecting a new channel, the bot will delete the one that was created during the first time setup should it still exist."""
    if not isinstance(value, discord.Role):
        await channel.send(f"{bot.cross} The admin role must be a Discord role in this server.")
    elif value.name == "@everyone":
        await channel.send(f"{bot.cross} The everyone role can not be used as the admin role.")
    elif value.name == "@here":
        await channel.send(f"{bot.cross} The here role can not be used as the admin role.")
    elif value.position > channel.guild.me.top_role.position:
        await channel.send(
            f"{bot.cross} The given role can not be used as the admin role as it is above {common.BOT_NAME}'s top role in the role hierarchy."
        )
    else:
        await bot.db.execute("UPDATE guild_config SET admin_role_id = ? WHERE guildId = ?", value.id, channel.guild.id)
        await channel.send(f"{bot.tick} The admin role has been set to {value.mention}.")
        lc = await retrieve.log_channel(bot, channel.guild)
        await lc.send(f"{bot.info} The admin role has been set to {value.mention}.")

        if (
            channel.guild.me.guild_permissions.manage_roles
            and (dar := await retrieve.system__defaultadminrole(bot, channel.guild)) is not None
        ):
            await dar.delete(reason="Default admin role was overridden.")
            lc = await retrieve.log_channel(bot, channel.guild)
            await lc.send(f"{bot.info} The default admin role has been deleted, as it is no longer required.")                       

