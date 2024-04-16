import random
import traceback
import typing

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

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
        user: typing.Optional[typing.Union[discord.Member, discord.User]],
        service: typing.Optional[str],
    ):

        if user and not service:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT * from music WHERE user_id = $1", user_id)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT * from music")

            url = random.choice(proper_urls)

            user = self.bot.get_user(url.user_id)

            name = f"User Songs"
            value = f"{user}"

        elif service and not user:
            proper_urls = await self.bot.db.fetch("SELECT * from music WHERE service = $1", service)
            url = random.choice(proper_urls)

            name = "Service Songs"
            value = f"{url.service}"

            user = self.bot.get_user(url.user_id)

        elif service and user:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT * from music WHERE service = $1 and user_id = $2", service, user_id)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT * from music WHERE service = $1", service)

                if not proper_urls:

                    proper_urls = await self.bot.db.fetch("SELECT * from music")

            url = random.choice(proper_urls)

            user = self.bot.get_user(url.user_id)

            name = "User and Service Songs"
            value = f"{user}"

        else:
            proper_urls = await self.bot.db.fetch("SELECT * from music")

            url = random.choice(proper_urls)

            name = "Randomly Choosen"
            value = f"\U0001f570"
        
            user = self.bot.get_user(url.user_id)

        if not user:
            user = "Unknown"

        embed = discord.Embed(title="Random Song", description=f"Service:\n{url.service} \nAdded By: \n{user}")

        embed.add_field(name=name, value=value)

        await interaction.response.send_message(content=url.url, embed=embed)

        # this definetly needs cleanup

    @find_song.autocomplete("service")
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):

        services = self.bot.services

        all_choices = [Choice(name=service.service, value=service.service) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith
    
    @app_commands.command(description="gets a song without any arguments", name="quicksong")
    async def quicksong(self, interaction: discord.Interaction):

        proper_urls = await self.bot.db.fetch("SELECT * from music")

        url = random.choice(proper_urls)

        user = self.bot.get_user(url.user_id)

        await interaction.response.send_message(f"Song: {url.url}\nAdded by {user}\nservice:{url.service}")

    @app_commands.command(description="gets a random video from the database", name="quickvideo")
    async def quickvideo(self, interaction: discord.Interaction):

        proper_urls = await self.bot.db.fetch("SELECT * from watched_videos")
        url = random.choice(proper_urls)

        user = self.bot.get_user(url.user_id)
        await interaction.response.send_message(f"Song: {url.url}\nAdded by {user}\nService:{url.service}")

    @app_commands.command(description="gets a random unwatched video from the database", name="quickwatch")
    async def quickwatch(self, interaction: discord.Interaction):

        proper_urls = await self.bot.db.fetch("SELECT * from to_watch")

        url = random.choice(proper_urls)
        user = self.bot.get_user(url.user_id)
        await interaction.response.send_message(f"Song: {url.url}\nAdded by {user}\nService:{url.service}")

    @app_commands.command(description="gets a random I don't know video from the database", name="quickidk")
    async def quickidk(self, interaction: discord.Interaction):

        proper_urls = await self.bot.db.fetch("SELECT * from idk_videos")

        url = random.choice(proper_urls)
        user = self.bot.get_user(url.user_id)
        await interaction.response.send_message(f"Song: {url.url}\nAdded by {user}\nService:{url.service}")

    @app_commands.command(description="gets a random Tech video from the database", name="quicktech")
    async def quicktech(self, interaction: discord.Interaction):

        proper_urls = await self.bot.db.fetch("SELECT * from tech_videos")

        url = random.choice(proper_urls)
        user = self.bot.get_user(url.user_id)
        await interaction.response.send_message(f"Song: {url.url}\nAdded by {user}\nService:{url.service}")

    async def cog_app_command_error(self, interaction, error):
        await interaction.response.send_message(error)
        traceback.print_exc(error)

        # there lol.


async def setup(bot):
    await bot.add_cog(Find(bot))
