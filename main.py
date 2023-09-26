import os
import traceback
from typing import Any

import asqlite
import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs import EXTENSIONS

import utils


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

        self.db = await asqlite.connect("database.db")

        main_cursor = await self.db.cursor()

        result = await main_cursor.execute("SELECT DISTINCT Service FROM data")

        services = await result.fetchall()
        self.services = [utils.ServiceObject(dict(x)["Service"]) for x in services]

    async def close(self) -> None:
        if self.db:
            await self.db.close()
        await super().close()


bot = MusicFinderBot(command_prefix=commands.when_mentioned_or("sb$"), intents=discord.Intents.all(), strip_after_prefix=True)

@bot.event
async def on_ready():
    print(bot.user)
    print(bot.id)


# so far this.

load_dotenv()
bot.run(os.environ["TOKEN"])