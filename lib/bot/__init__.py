from asyncio import sleep
import os

from discord.errors import Forbidden, HTTPException
from discord.ext.commands.context import Context
import common
from glob import glob
from datetime import date, datetime 
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands.errors import BadArgument, CommandNotFound, CommandOnCooldown, MissingRequiredArgument
from discord import Embed, File
from discord.ext.commands import Bot as BotBase
from lib.db import dal

COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORED_EXCEPTIONS = (CommandNotFound, BadArgument)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
            print(f"{cog} cog ready")

    def ready_up(self, cog):
        setattr(self, cog, True)

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = common.DEFAULT_PREFIXES
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        load_dotenv()
        self.DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  

        dal.autosave(self.scheduler)
        super().__init__(
            command_prefix=self.PREFIX,
            owner_ids=common.OWNER_IDS, 
            name=common.BOT_NAME, 
            description=f"{common.BOT_NAME}. Your note taking bot."
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} loaded")
        print("Setup complete")

    def run(self, version):
        self.VERSION = version

        print("Running setup...")
        self.setup()

        print("Running bot...")
        super().run(self.DISCORD_TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if self.ready:
            if ctx.command is not None and ctx.guild is not None:
                await self.invoke(ctx)
        else:
            await ctx.send("Not ready for commands")

    async def rules_reminder(self):
        await self.stdout.send("Don't forget the rules!")

    async def on_connect(self):
        print("Bot connected")

    async def on_disconnect(self):
        print("Bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong")
        await self.stdout.send("An error occurred")
        raise

    async def on_command_error(self, ctx, error: Exception):
        if(any([isinstance(error, ex) for ex in IGNORED_EXCEPTIONS])):
            pass

        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing")

        elif isinstance(error, CommandOnCooldown):
            await ctx.send(f"That command is on {str(error.cooldown.type).split('.')[-1]} cooldown. Please try again in {error.retry_after:,.2f} seconds.")

        elif hasattr(error, "original_error"):

            # elif isinstance(error.original_error, HTTPException):
            #     await ctx.send("Unable to send message")
            if isinstance(error.original_error, Forbidden):
                await ctx.send("I do not have permission to do that.")
            else:
                raise error

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(common.MY_GUILD_ID)
            self.stdout = self.get_channel(common.MSG_CHANNEL)
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()
            
            # embed = Embed(title="Now online!", description=f"{common.BOT_NAME} is online and ready to take notes.", 
            #                 color=0xFF0000, timestamp=datetime.utcnow(), icon_url=self.guild.icon_url)
            # fields = [("Name", "Value", True),
            #             ("Other", "This field appears next to first", True),
            #             ("Non-inline", "Appears on its own row", False)]
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)
            # embed.set_author(name="Erisia Web Development")
            # embed.set_footer(text=f"{common.BOT_NAME} Help")
            # embed.set_thumbnail(url=self.guild.icon_url)
            # embed.set_image(url=self.guild.icon_url)
            # await channel.send(embed=embed)
            # await channel.send(file=File("./data/images/bot_image.png"))

            while not self.cogs_ready.all_ready():
                await sleep(0, 5)
            await self.stdout.send("Now online!")

            self.ready = True
            print("Bot ready")
        else:
            print("Bot reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()