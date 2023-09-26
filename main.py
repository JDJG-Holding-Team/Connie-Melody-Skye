import os
import traceback
from typing import Any

import asqlite
import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs import EXTENSIONS


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

    async def close(self) -> None:
        if self.db:
            await self.db.close()
        await super().close()


bot = MusicFinderBot(command_prefix=commands.when_mentioned_or("e$"), intents=discord.Intents.all(), strip_after_prefix=True)


# so far this.

load_dotenv()
bot.run(os.environ["TOKEN"])