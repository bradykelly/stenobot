import os
import common
from datetime import date, datetime 
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File
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

            channel = self.get_channel(737356948676018297)
            embed = Embed(title="Now online!", description=f"{common.BOT_NAME} is online and ready to take notes.", 
                            color=0xFF0000, timestamp=datetime.utcnow(), icon_url=self.guild.icon_url)
            fields = [("Name", "Value", True),
                        ("Other", "This field appears next to first", True),
                        ("Non-inline", "Appears on its own row", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="Erisia Web Development")
            embed.set_footer(text=f"{common.BOT_NAME} Help")
            embed.set_thumbnail(url=self.guild.icon_url)
            embed.set_image(url=self.guild.icon_url)
            await channel.send(embed=embed)

            await channel.send(file=File("./data/images/bot_image.png"))
        else:
            print("Bot reconnected")

    async def on_message(self, message):
        pass


bot = Bot()