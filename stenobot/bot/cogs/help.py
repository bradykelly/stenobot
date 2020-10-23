# From Solaris: https://github.com/parafoxia/Solaris

import datetime as dt
import typing as t
import common
from collections import defaultdict
from discord.ext import commands
from discord.ext.commands.cog import Cog
from stenobot.utils import chron, converters, menu, string


class HelpMenu(menu.MultiPageMenu):
    def __init__(self, ctx, pagemaps):
        super().__init__(ctx, pagemaps, timeout=common.MENU_TIMEOUT2)


class Help(commands.Cog):
    """Assistance with using this bot."""

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @staticmethod
    async def basic_syntax(ctx, cmd, prefix):
        try:
            await cmd.can_run(ctx)
            return f"{cmd.name}" if cmd.parent is None else f"  ↳ {cmd.name}"
        except commands.CommandError:
            return f"{cmd.name} (✗)" if cmd.parent is None else f"  ↳ {cmd.name} (✗)"

    @staticmethod
    def full_syntax(ctx, cmd, prefix):
        invokations = "|".join([cmd.name, *cmd.aliases])
        if (p := cmd.parent) is None:
            return f"```{invokations} {cmd.signature}```"
        else:
            p_invokations = "|".join([p.name, *p.aliases])
            return f"```{p_invokations} {invokations} {cmd.signature}```"

    @staticmethod
    async def required_permissions(ctx, cmd):
        try:
            await cmd.can_run(ctx)
            return "Yes"
        except commands.MissingPermissions as exc:
            mp = string.list_of([str(perm.replace("_", " ")).title() for perm in exc.missing_perms])
            return f"No - You are missing the {mp} permission(s)"
        except commands.BotMissingPermissions as exc:
            mp = string.list_of([str(perm.replace("_", " ")).title() for perm in exc.missing_perms])
            return f"No - {common.BOT_NAME} is missing the {mp} permission(s)"
        except commands.CommandError:
            return f"No - {common.BOT_NAME} is not set up properly"

    async def get_command_mapping(self, ctx):
        mapping = defaultdict(list)

        for cog in self.bot.cogs.values():
            if cog.__doc__ is not None:
                for cmd in cog.walk_commands():
                    if cmd.help is not None:
                        mapping[cog].append(cmd)

        return mapping

    @commands.command(
        name="help",
        help=f"Help with anything {common.BOT_NAME}. Passing a command name or alias through will show help with that specific command, while passing no arguments will bring up a general command overview.",
    )
    async def help_command(self, ctx, *, cmd: t.Optional[t.Union[converters.Command, str]]):
        prefix = await self.bot.prefix(ctx.guild)

        if isinstance(cmd, str):
            await ctx.send(f"{self.bot.cross} {common.BOT_NAME} has no commands or aliases with that name.")

        elif isinstance(cmd, commands.Command):
            await ctx.send(
                embed=self.bot.embed.build(
                    ctx=ctx,
                    header="Help",
                    description=cmd.help,
                    thumbnail=self.bot.user.avatar_url,
                    fields=(
                        ("Syntax (<required> • [optional])", self.full_syntax(ctx, cmd, prefix), False),
                        ("Command Prefix:", prefix, False),
                    ),
                )
            )

        else:
            pagemaps = []

            for cog, cmds in (await self.get_command_mapping(ctx)).items():
                pagemaps.append(
                    {
                        "header": "Help",
                        "title": f"The `{cog.qualified_name.lower()}` module",
                        "description": f"{cog.__doc__}\n\nUse `{prefix}help [command]` for more detailed help on a command. You can not run commands with `(✗)` next to them.",
                        "thumbnail": self.bot.user.avatar_url,
                        "fields": (
                            (
                                f"{len(cmds)} command(s)",
                                "```{}```".format(
                                    "\n" + "\n".join([await self.basic_syntax(ctx, cmd, prefix) for cmd in cmds])
                                ),
                                False,
                            ),
                        ),
                    }
                )

            await HelpMenu(ctx, pagemaps).start()
        
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready.booted:
            self.bot.ready.up(self)            


def setup(bot):
    bot.add_cog(Help(bot))
