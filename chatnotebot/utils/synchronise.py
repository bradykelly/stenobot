
import discord
from chatnotebot.utils import chron


class Okay:
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild


class Synchronise:
    def __init__(self, bot):
        self.bot = bot

    async def reactions(self, guild, gm, accepted):
        tick = gm.reactions[0]
        cross = gm.reactions[1]
        ticked = await tick.users().flatten()
        crossed = await cross.users().flatten()
        ticked_and_left = set(ticked) - set(guild.members)
        crossed_and_left = set(crossed) - set(guild.members)

        for user in ticked_and_left:
            await gm.remove_reaction(tick.emoji, user)

        for user in crossed_and_left:
            await gm.remove_reaction(cross.emoji, user)

        for user in crossed:
            if user.id in accepted:
                await gm.remove_reaction(cross.emoji, user)

    async def on_boot(self):
        last_commit = chron.from_iso(await self.bot.db.field("SELECT Value FROM bot WHERE Key = 'last commit'"))
        #TODO Get rid of gateway stuff.
        records = await self.bot.db.records(
            "SELECT GuildID, RulesChannelID, GateMessageID, BlockingRoleID, MemberRoleIDs, ExceptionRoleIDs FROM gateway WHERE Active = 1"
        )

        entrants = {
            guild_id: [int(user_id) for user_id in user_ids.split(",")]
            for guild_id, user_ids in await self.bot.db.records(
                "SELECT GuildID, GROUP_CONCAT(UserID) FROM entrants GROUP BY GuildID"
            )
        }

        accepted = {
            guild_id: [int(user_id) for user_id in user_ids.split(",")]
            for guild_id, user_ids in await self.bot.db.records(
                "SELECT GuildID, GROUP_CONCAT(UserID) FROM accepted GROUP BY GuildID"
            )
        }
        for guild_id, rc_id, gm_id, br_id, mr_ids, er_ids in records:
            guild = self.bot.get_guild(guild_id)
            okay = Okay(self.bot, guild)

        await self.bot.db.execute("UPDATE entrants SET Timeout = datetime('now', '+3600 seconds')")
