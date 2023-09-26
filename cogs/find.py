import random
import typing

import discord

from discord import app_commands
from discord.ext import commands

from discord.app_commands import Choice


class Find(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_unload(self):
        return
        # use for later.

    @app_commands.command(description="Find a new song to listen to", name="find")
    async def find_song(
        self,
        interaction: discord.Interaction,
        user : typing.Optional[typing.Union[discord.Member, discord.User]],
        service : typing.Optional[str],
    ):
        
        cur = await self.bot.db.cursor()

        if service:
            result = await cur.execute("SELECT url from data WHERE service = ?", service)
            
            urls = await result.fetchall()

            proper_urls = [utils.DataObject(dict(url)) for url in urls]

            print(proper_urls)


    @find_song.autocomplete('service')
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):

        services = self.bot.services
        
        all_choices = [Choice(name=service.name, value=service.name) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith


async def setup(bot):
    await bot.add_cog(Find(bot))