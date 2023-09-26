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

    @app_commands.command(description="Find a new song to listen to", name="find_song")
    async def find_song(
        self,
        user : typing.Optional[typing.Union[discord.Member, discord.User]],
        Service : typing.Optional[str],
    ):
        

        await interaction.response.send_message(f"{Service}")


    @find_song.autocomplete('Service')
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):

        services = self.bot.services
        
        all_choices = [Choice(name=service) for service  in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith


async def setup(bot):
    await bot.add_cog(Find(bot))