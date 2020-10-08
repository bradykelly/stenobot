# From Solaris: https://github.com/parafoxia/Solaris/blob/master/solaris/utils/__init__.py

from collections import deque

from apscheduler.triggers.cron import CronTrigger
from discord import Activity, ActivityType

ACTIVITY_TYPES = ("playing", "watching", "listening", "streaming")


class PresenceSetter:
    def __init__(self, bot):
        self.bot = bot

        self._name = "@Solaris help • {message} • Version {version}"
        self._type = "watching"
        self._messages = deque(
            (
                "Invite Solaris to your server by using @Solaris invite",
                "To view information about Solaris, use @Solaris botinfo",
                "Need help with Solaris? Join the support server! Use @Solaris support to get an invite",
                "Developed by Parafoxia#1911, and available under the GPLv3 license",
            )
        )

        self.bot.scheduler.add_job(self.set, CronTrigger(second=0))

    @property
    def name(self):
        message = self._messages[0].format(bot=self.bot)
        return self._name.format(message=message, version=self.bot.version)

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def type(self):
        return getattr(ActivityType, self._type, ActivityType.playing)

    @type.setter
    def type(self, value):
        if value not in ACTIVITY_TYPES:
            raise ValueError("The activity should be one of the following: {}".format(", ".join(ACTIVITY_TYPES)))

        self._type = value

    async def set(self):
        await self.bot.change_presence(activity=Activity(name=self.name, type=self.type))
        self._messages.rotate(-1)
