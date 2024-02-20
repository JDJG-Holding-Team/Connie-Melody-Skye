import os
import traceback
from typing import Any

import asqlite
import asyncpg
import discord
from discord.ext import commands
from dotenv import load_dotenv

import utils
from cogs import EXTENSIONS

class CustomRecordClass(asyncpg.Record):
    def __getattr__(self, name: str) -> Any:
        if name in self.keys():
            return self[name]
        return super().__getattr__(name)


class MusicFinderBot(commands.Bot):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        for cog in EXTENSIONS:
            try:
                await self.load_extension(f"{cog}")
            except commands.errors.ExtensionError:
                traceback.print_exc()

        await self.load_extension("jishaku")

        self.old_db = await asqlite.connect("database.db")
        self.db = await asyncpg.create_pool(os.getenv("DB_key"), record_class=CustomRecordClass)

        main_cursor = await self.old_db.cursor()

        result = await main_cursor.execute("SELECT DISTINCT Service FROM music")
        self.services = await self.db.fetch("SELECT DISTINCT Service FROM music")

        services_old = await result.fetchall()
        self.services_old = [utils.DataObject(dict(x)) for x in services2]

    async def close(self) -> None:
        if self.db:
            await self.db.close()
        
        if self.old_db:
            await self.old_db.close()
        
        await super().close()


bot = MusicFinderBot(
    command_prefix=commands.when_mentioned_or("sb$"), intents=discord.Intents.all(), strip_after_prefix=True
)


@bot.event
async def on_ready():
    print(bot.user)
    print(bot.user.id)


# so far this.

load_dotenv()
bot.run(os.environ["TOKEN"])
