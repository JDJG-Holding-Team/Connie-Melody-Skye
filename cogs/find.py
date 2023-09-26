import random
import typing

import discord

from discord import app_commands
from discord.ext import commands


class Find(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_unload(self):
        return
        # use for later.

    


async def setup(bot):
    await bot.add_cog(Find(bot))