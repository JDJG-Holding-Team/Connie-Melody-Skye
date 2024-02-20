import os
import sys
import traceback
from typing import Any

import asyncpg
import discord
from discord.ext import commands
from dotenv import load_dotenv

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

        self.db = await asyncpg.create_pool(os.getenv("DB_key"), record_class=CustomRecordClass)

        self.services = await self.db.fetch("SELECT DISTINCT service FROM music")

    async def close(self) -> None:
        if self.db:
            await self.db.close()
        
        await super().close()

    async def on_error(self, event, *args: Any, **kwargs: Any) -> None:
        more_information = sys.exc_info()
        error_wanted = traceback.format_exc()
        traceback.print_exc()

        # print(event)
        # print(more_information[0])
        # print(args)
        # print(kwargs)
        # check about on_error with other repos of mine as well to update this.


bot = MusicFinderBot(
    command_prefix=commands.when_mentioned_or("sb$"), intents=discord.Intents.all(), strip_after_prefix=True
)


@bot.event
async def on_ready():
    print(bot.user)
    print(bot.user.id)


# so far this.
    
if not os.getenv("TOKEN"):
    load_dotenv()
    print("I Ran yeah")


bot.run(os.environ["TOKEN"])
