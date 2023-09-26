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
    async def member_update(
        self,
        user : typing.Optional[typing.Union[discord.Member, discord.User]],
        Service : str
    ):
        await interaction.response.send_message("Test")


    @member_update.autocomplete('Service')
    async def autocomplete_callback(interaction: discord.Interaction, current: str):

        services = self.bot.services
        
        # all_choices = [Choice(name=name, value=link) for  in service.items()]
        #startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        # if not (current and startswith):
            # return all_choices[0:25]

        # return startswith


async def setup(bot):
    await bot.add_cog(Find(bot))