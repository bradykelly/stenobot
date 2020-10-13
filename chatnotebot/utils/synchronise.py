
import discord
from chatnotebot.utils import chron, trips


class Okay:
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild

    async def permissions(self):
        if not self.guild.me.guild_permissions.manage_roles:
            await trips.gateway(self, "Solaris no longer has the Manage Roles permission")
        elif not self.guild.me.guild_permissions.kick_members:
            await trips.gateway(self, "Solaris no longer has the Kick Members permission")
        else:
            return True

    async def gate_message(self, rc_id, gm_id):
        try:
            if (rc := self.bot.get_channel(rc_id)) is None:
                await trips.gateway(self, "the rules channel no longer exists, or is unable to be accessed by Solaris")
            else:
                # This is done here to ensure the correct order of operations.
                gm = await rc.fetch_message(gm_id)

                if not rc.permissions_for(self.guild.me).manage_messages:
                    await trips.gateway(
                        self, "Solaris does not have the Manage Messages permission in the rules channel"
                    )
                else:
                    return gm

        except discord.NotFound:
            await trips.gateway(self, "the gate message no longer exists")

    async def blocking_role(self, br_id):
        if (br := self.guild.get_role(br_id)) is None:
            await trips.gateway(self, "the blocking role no longer exists, or is unable to be accessed by Solaris")
        elif br.position >= self.guild.me.top_role.position:
            await trips.gateway(
                self, "the blocking role is equal to or higher than Solaris' top role in the role hierarchy"
            )
        else:
            return br

    async def member_roles(self, mr_ids):
        if mr_ids is not None:
            for r in (mrs := [self.guild.get_role(int(id_)) for id_ in mr_ids.split(",")]) :
                if r is None:
                    await trips.gateway(
                        self, "one or more member roles no longer exist, or are unable to be accessed by Solaris"
                    )
                    return
                elif r.position >= self.guild.me.top_role.position:
                    await trips.gateway(
                        self,
                        "one or more member roles are equal to or higher than Solaris' top role in the role hierarchy",
                    )
                    return

            return mrs

    async def exception_roles(self, er_ids):
        if er_ids is not None:
            for r in (ers := [self.guild.get_role(int(id_)) for id_ in er_ids.split(",")]) :
                if r is None:
                    await trips.gateway(
                        self, "one or more exception roles no longer exist, or are unable to be accessed by Solaris"
                    )
                    return

            return ers

    async def welcome_channel(self, wc_id):
        if wc_id is not None:
            if (wc := self.bot.get_channel(wc_id)) is None:
                await trips.gateway(
                    self, "the welcome channel no longer exists or is unable to be accessed by Solaris"
                )
            elif not wc.permissions_for(self.guild.me).send_messages:
                await trips.gateway(self, "Solaris does not have the Send Messages permission in the welcome channel")
            else:
                return wc

    async def goodbye_channel(self, gc_id):
        if gc_id is not None:
            if (gc := self.bot.get_channel(gc_id)) is None:
                await trips.gateway(
                    self, "the goodbye channel no longer exists or is unable to be accessed by Solaris"
                )
            elif not gc.permissions_for(self.guild.me).send_messages:
                await trips.gateway(self, "Solaris does not have the Send Messages permission in the goodbye channel")
            else:
                return gc



class Synchronise:
    def __init__(self, bot):
        self.bot = bot

    async def _allow(self, okay, member, br_id, mr_ids):
        if (mrs := await okay.member_roles(mr_ids)) and (unassigned := set(mrs) - set(member.roles)):
            await member.add_roles(
                *list(unassigned),
                reason="Member accepted the server rules (performed during synchronisation).",
                atomic=False,
            )

        if (br := await okay.blocking_role(br_id)) in member.roles:
            await member.remove_roles(
                br,
                reason="Member accepted the server rules, or was given an exception role (performed during synchronisation).",
            )

    async def _deny(self, okay, member, br_id):
        await member.kick(reason="Member declined the server rules (performed during synchronisation).")

    async def members(self, guild, okay, gm, br_id, mr_ids, er_ids, last_commit, entrants, accepted):
        def _check(m):
            return not m.bot and (m.joined_at > last_commit or m.id in entrants)

        reacted = []
        new = []
        left = []

        ticked = await gm.reactions[0].users().flatten()
        crossed = await gm.reactions[1].users().flatten()
        ers = await okay.exception_roles(er_ids) or []

        for member in filter(lambda m: _check(m), guild.members):
            if member in ticked:
                await self._allow(okay, member, br_id, mr_ids)
                reacted.append((guild.id, member.id))
                new.append((guild.id, member.id))
            elif member in crossed:
                await self._deny(okay, member, br_id)
                reacted.append((guild.id, member.id))
            elif any(r in member.roles for r in ers):
                await self._allow(okay, member, br_id, mr_ids)
                reacted.append((guild.id, member.id))

        for user_id in set([*entrants, *accepted]):
            if not guild.get_member(user_id):
                left.append((guild.id, user_id))

        await self.bot.db.executemany("DELETE FROM entrants WHERE GuildID = ? AND UserID = ?", set([*reacted, *left]))
        await self.bot.db.executemany("DELETE FROM accepted WHERE GuildID = ? AND UserID = ?", set(left))
        await self.bot.db.executemany("INSERT OR IGNORE INTO accepted VALUES (?, ?)", set(new))

    async def roles(self, guild, okay, br_id, mr_ids, accepted, accepted_only):
        def _check(m):
            return not m.bot and (not accepted_only or m.id in accepted)

        br = await okay.blocking_role(br_id)
        mrs = await okay.member_roles(mr_ids)

        for member in filter(lambda m: _check(m), guild.members):
            if br not in member.roles and (unassigned := set(mrs) - set(member.roles)):
                await member.add_roles(
                    *list(unassigned),
                    reason="Member roles have been updated (performed during synchronisation).",
                    atomic=False,
                )

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
        records = await self.bot.db.records(
            "SELECT GuildID, rulesChannelId, GateMessageID, BlockingRoleID, MemberRoleIDs, ExceptionRoleIDs FROM gateway WHERE Active = 1"
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

            if gm := await okay.gate_message(rc_id, gm_id):
                await self.members(
                    guild,
                    okay,
                    gm,
                    br_id,
                    mr_ids,
                    er_ids,
                    last_commit,
                    entrants.get(guild_id, []),
                    accepted.get(guild_id, []),
                )

        await self.bot.db.execute("UPDATE entrants SET Timeout = datetime('now', '+3600 seconds')")
