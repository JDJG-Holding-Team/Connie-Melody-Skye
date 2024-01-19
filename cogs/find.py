import random
import typing

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

import utils


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

        cur = await self.bot.db.cursor()

        if user and not service:

            user_id = user.id

            result = await cur.execute("SELECT * from data WHERE user_id = ?", user_id)

            urls = await result.fetchall()

            proper_urls = [utils.DataObject(dict(url)) for url in urls]

            if not proper_urls:

                result = await cur.execute("SELECT * from data")

                urls = await result.fetchall()

                proper_urls = [utils.DataObject(dict(url)) for url in urls]

            url = random.choice(proper_urls)

            user = self.bot.get_user(url.user_id)

            name = f"User Songs"
            value = f"{user}"

        elif service and not user:
            result = await cur.execute("SELECT * from data WHERE service = ?", service)

            urls = await result.fetchall()

            proper_urls = [utils.DataObject(dict(url)) for url in urls]

            url = random.choice(proper_urls)

            name = "Service Songs"
            value = f"{url.Service}"

            user = self.bot.get_user(url.user_id)

        elif service and user:

            user_id = user.id

            result = await cur.execute("SELECT * from data WHERE service = ? and user_id = ?", service, user_id)

            urls = await result.fetchall()

            proper_urls = [utils.DataObject(dict(url)) for url in urls]

            if not proper_urls:

                result = await cur.execute("SELECT * from data WHERE service = ?", service)

                urls = await result.fetchall()

                proper_urls = [utils.DataObject(dict(url)) for url in urls]

                if not proper_urls:

                    result = await cur.execute("SELECT * from data")

                    urls = await result.fetchall()

                    proper_urls = [utils.DataObject(dict(url)) for url in urls]

            url = random.choice(proper_urls)

            user = self.bot.get_user(url.user_id)

            name = "User and Service Songs"
            value = f"{user}"

        else:
            result = await cur.execute("SELECT * from data")

            urls = await result.fetchall()

            proper_urls = [utils.DataObject(dict(url)) for url in urls]

            url = random.choice(proper_urls)

            name = "Randomly Choosen"
            value = f"\U0001f570"
        
            user = self.bot.get_user(url.user_id)

        if not user:
            user = "Unknown"

        embed = discord.Embed(title="Random Song", description=f"Service:\n{url.Service} \nAdded By: \n{user}")

        embed.add_field(name=name, value=value)

        await interaction.response.send_message(content=url.url, embed=embed)

        # this definetly needs cleanup

    @find_song.autocomplete("service")
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):

        services = self.bot.services

        all_choices = [Choice(name=service.Service, value=service.Service) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith
    
    @app_commands.command(description="gets a song without any arguments", name="quicksong")
    async def quicksong(self, interaction: discord.Interaction):

        cur = await self.bot.db.cursor()

        result = await cur.execute("SELECT * from data")

        urls = await result.fetchall()

        proper_urls = [utils.DataObject(dict(url)) for url in urls]

        url = random.choice(proper_urls)

        user = self.bot.get_user(url.user_id)

        await interaction.response.send_message(f"Song: {url.url}\nAdded by {user}\nService:{url.Service}")

    @app_commands.command(description="gets a random video from the database", name="quickvideo")
    async def quickvideo(self, interaction: discord.Interaction):

        cur = await self.bot.db.cursor()

        result = await cur.execute("SELECT * from watched_videos")

        urls = await result.fetchall()

        proper_urls = [utils.DataObject(dict(url)) for url in urls]

        url = random.choice(proper_urls)

        user = self.bot.get_user(url.user_id)

        await interaction.response.send_message(f"Song: {url.url}\nAdded by {user}\nService:{url.service}")

    @app_commands.command(description="gets a random unwatched video from the database", name="quickwatch")
    async def quickwatch(self, interaction: discord.Interaction):

        cur = await self.bot.db.cursor()

        result = await cur.execute("SELECT * from to_watch")

        urls = await result.fetchall()

        proper_urls = [utils.DataObject(dict(url)) for url in urls]

        url = random.choice(proper_urls)

        user = self.bot.get_user(url.user_id)

        await interaction.response.send_message(f"Song: {url.url}\nAdded by {user}\nService:{url.Service}")


async def setup(bot):
    await bot.add_cog(Find(bot))
