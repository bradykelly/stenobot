import os
import common
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = common.DEFAULT_PREFIXES
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        load_dotenv()
        self.DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

        super().__init__(
            command_prefix=self.PREFIX,
            owner_ids=common.OWNER_IDS, 
            name=common.BOT_NAME, 
            description=f"{common.BOT_NAME}. Your note taking bot."
        )

    def run(self, version):
        self.VERSION = version
        print("Running bot...")
        super().run(self.DISCORD_TOKEN, reconnect=True)

    async def on_connect(self):
        print("Bot connected")

    async def on_disconnect(self):
        print("Bot disconnected")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(common.MY_GUILD_ID)
            print("Bot ready")
        else:
            print("Bot reconnected")

    async def on_message(self, message):
        pass


bot = Bot()