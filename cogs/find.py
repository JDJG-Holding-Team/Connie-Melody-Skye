from __future__ import annotations

import random
import traceback
import typing

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from utils.extra import ContentType, database_lookup

if typing.TYPE_CHECKING:
    from main import ConnieSkye


class Find(commands.Cog):

    def __init__(self, bot: ConnieSkye) -> None:
        self.bot: ConnieSkye = bot

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Find a new song to listen to", name="find_song")
    async def find_song(
        self,
        interaction: discord.Interaction,
        user: typing.Optional[typing.Union[discord.Member, discord.User]],
        service: typing.Optional[str],
    ):
        content_type = ContentType.music
        result = await database_lookup(self.bot, content_type, user, service)
        user = result.user or "Unknown"
        await interaction.response.send_message(content=f"Song: {result.url}\nService: {result.service}\nAdded By: {user} \n{result.name} {result.value}")

    @find_song.autocomplete("service")
    async def find_song_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM content where content_type = $1", ContentType.music.value)

        all_choices = [Choice(name=service.service, value=service.service) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith[0:25]

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Find a new video that's misc.", name="find_misc")
    async def find_misc(
        self,
        interaction: discord.Interaction,
        user: typing.Optional[typing.Union[discord.Member, discord.User]],
        service: typing.Optional[str],
    ):

        content_type = ContentType.misc
        result = await database_lookup(self.bot, content_type, user, service)
        user = result.user or "Unknown"
        await interaction.response.send_message(content=f"Video: {result.url}\nService: {result.service}\nAdded By: {user} \n{result.name} {result.value}")

    @find_misc.autocomplete("service")
    async def find_misc_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM content where content_type = $1", ContentType.misc.value)

        all_choices = [Choice(name=service.service, value=service.service) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith[0:25]

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Find a new video to watch in my technology videos", name="find_tech")
    async def find_tech(
        self,
        interaction: discord.Interaction,
        user: typing.Optional[typing.Union[discord.Member, discord.User]],
        service: typing.Optional[str],
    ):
        content_type = ContentType.tech
        result = await database_lookup(self.bot, content_type, user, service)
        user = result.user or "Unknown"
        await interaction.response.send_message(content=f"Video: {result.url}\nService: {result.service}\nAdded By: {user} \n{result.name} {result.value}")

    @find_tech.autocomplete("service")
    async def find_tech_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM content where content_type = $1", ContentType.tech.value)

        all_choices = [Choice(name=service.service, value=service.service) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith[0:25]

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Find a new video to watch in my watched videos", name="find_watched")
    async def find_watched(
        self,
        interaction: discord.Interaction,
        user: typing.Optional[typing.Union[discord.Member, discord.User]],
        service: typing.Optional[str],
    ):
        content_type = ContentType.watched
        result = await database_lookup(self.bot, content_type, user, service)
        user = result.user or "Unknown"
        await interaction.response.send_message(content=f"Video: {result.url}\nService: {result.service}\nAdded By: {user} \n{result.name} {result.value}")
        

    @find_watched.autocomplete("service")
    async def find_watched_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM content where content_type = $1", ContentType.watched.value)
        all_choices = [Choice(name=service.service, value=service.service) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith[0:25]

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Find a new video to watch in my to watch videos", name="find_to_watch")
    async def find_to_watch(
        self,
        interaction: discord.Interaction,
        user: typing.Optional[typing.Union[discord.Member, discord.User]],
        service: typing.Optional[str],
    ): 
        content_type = ContentType.watch
        result = await database_lookup(self.bot, content_type, user, service)
        user = result.user or "Unknown"
        await interaction.response.send_message(content=f"Video: {result.url}\nService: {result.service}\nAdded By: {user} \n{result.name} {result.value}")

    @find_to_watch.autocomplete("service")
    async def find_watch_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM content where content_type = $1", ContentType.watch.value)

        all_choices = [Choice(name=service.service, value=service.service) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith[0:25]

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Gets a song without any arguments", name="quick_song")
    async def quick_song(self, interaction: discord.Interaction[ConnieSkye]):

        url = await self.bot.db.fetchrow("SELECT user_id, url, service from content where content_type = $1 ORDER BY RANDOM()", ContentType.music.value)
        user = await self.bot.try_user(url.user_id)

        content = await self.bot.tree.translator.translate_content(
            interaction,
            "Song: {url_url}\nAdded by {user}\nService: {url_service}",
            url_url=url.url, user=user, url_service=url.service
        )
        await interaction.response.send_message(content)

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Gets a random video from the database", name="quick_video")
    async def quick_video(self, interaction: discord.Interaction):

        url = await self.bot.db.fetchrow("SELECT user_id, url, service from content where content_type = $1 ORDER BY RANDOM()", ContentType.watched.value)
        user = await self.bot.try_user(url.user_id)
        content = await self.bot.tree.translator.translate_content(
            interaction,
            "Video: {url_url}\nAdded by {user}\nService: {url_service}",
            url_url=url.url,
            user=user,
            url_service=url.service,
        )
        await interaction.response.send_message(content)

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Gets a random unwatched video from the database", name="quick_watch")
    async def quick_watch(self, interaction: discord.Interaction):

        url = await self.bot.db.fetchrow("SELECT user_id, url, service from content where content_type = $1 ORDER BY RANDOM()", ContentType.watch.value)
        user = await self.bot.try_user(url.user_id)
        content = await self.bot.tree.translator.translate_content(
            interaction,
            "Video: {url_url}\nAdded by {user}\nService: {url_service}",
            url_url=url.url,
            user=user,
            url_service=url.service,
        )
        await interaction.response.send_message(content)

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Gets a random misc video from the database", name="quick_misc")
    async def quick_misc(self, interaction: discord.Interaction):

        url = await self.bot.db.fetchrow("SELECT user_id, url, service from content where content_type = $1 ORDER BY RANDOM()", ContentType.misc.value)
        user = await self.bot.try_user(url.user_id)
        content = await self.bot.tree.translator.translate_content(
            interaction,
            "Video: {url_url}\nAdded by {user}\nService: {url_service}",
            url_url=url.url,
            user=user,
            url_service=url.service,
        )
        await interaction.response.send_message(content)

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Gets a random tech video from the database", name="quick_tech")
    async def quick_tech(self, interaction: discord.Interaction):

        url = await self.bot.db.fetchrow("SELECT user_id, url, service from content where content_type = $1 ORDER BY RANDOM()", ContentType.tech.value)
        user = await self.bot.try_user(url.user_id)
        content = await self.bot.tree.translator.translate_content(
            interaction,
            "Video: {url_url}\nAdded by {user}\nService: {url_service}",
            url_url=url.url,
            user=user,
            url_service=url.service,
        )
        await interaction.response.send_message(content)

    async def cog_app_command_error(self, interaction, error):
        await interaction.response.send_message(error)
        traceback.print_exc(error)

        # there lol.

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Gets a random anime video from the database", name="quick_anime")
    async def quick_anime(self, interaction: discord.Interaction):

        url = await self.bot.db.fetchrow("SELECT user_id, url, service from content where content_type = $1 ORDER BY RANDOM()", ContentType.anime.value)
        user = await self.bot.try_user(url.user_id)
        content = await self.bot.tree.translator.translate_content(
            interaction,
            "Video: {url_url}\nAdded by {user}\nService: {url_service}",
            url_url=url.url,
            user=user,
            url_service=url.service,
        )
        await interaction.response.send_message(content)

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(user="User who added/suggested the content.")
    @app_commands.describe(service="Service where it was added on.")
    @app_commands.command(description="Find a new video to watch in my to watch videos", name="find_anime")
    async def find_anime(
        self,
        interaction: discord.Interaction,
        user: typing.Optional[typing.Union[discord.Member, discord.User]],
        service: typing.Optional[str],
    ):
        content_type = ContentType.anime
        result = await database_lookup(self.bot, content_type, user, service)
        user = result.user or "Unknown"
        await interaction.response.send_message(content=f"Video: {result.url}\nService: {result.service}\nAdded By: {user} \n{result.name} {result.value}")
      

    @find_anime.autocomplete("service")
    async def find_anime_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM content where content_type = $1", ContentType.anime.value)

        all_choices = [Choice(name=service.service, value=service.service) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith[0:25]

    @app_commands.command()
    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def source(self, interaction: discord.Interaction):
        """Sends link to the bot's source code"""

        url = "https://github.com/JDJG-Holding-Team/Connie-Melody-Skye"
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Source",
                url=url,
                style=discord.ButtonStyle.link,
            )
        )
        await interaction.response.send_message(f"Source: {url}", view=view)

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Gets a random politics video from the database", name="quick_politics")
    async def quick_politics(self, interaction: discord.Interaction):

        url = await self.bot.db.fetchrow("SELECT user_id, url, service from content where content_type = $1 ORDER BY RANDOM()", ContentType.politics.value)
        user = await self.bot.try_user(url.user_id)
        content = await self.bot.tree.translator.translate_content(
            interaction,
            "Video: {url_url}\nAdded by {user}\nService: {url_service}",
            url_url=url.url,
            user=user,
            url_service=url.service,
        )
        await interaction.response.send_message(content)

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Find a new video that's politics related.", name="find_politics")
    async def find_politics(
        self,
        interaction: discord.Interaction,
        user: typing.Optional[typing.Union[discord.Member, discord.User]],
        service: typing.Optional[str],
    ):

        content_type = ContentType.politics
        result = await database_lookup(self.bot, content_type, user, service)
        user = result.user or "Unknown"
        await interaction.response.send_message(content=f"Video: {result.url}\nService: {result.service}\nAdded By: {user} \n{result.name} {result.value}")

    @find_politics.autocomplete("service")
    async def find_politics_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM content where content_type = $1", ContentType.politics.value)

        all_choices = [Choice(name=service.service, value=service.service) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith[0:25]

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Gets a random horror video from the database", name="quick_horror")
    async def quick_horror(self, interaction: discord.Interaction):

        url = await self.bot.db.fetchrow("SELECT user_id, url, service from content where content_type = $1 ORDER BY RANDOM()", ContentType.horror.value)
        user = await self.bot.try_user(url.user_id)
        content = await self.bot.tree.translator.translate_content(
            interaction,
            "Video: {url_url}\nAdded by {user}\nService: {url_service}",
            url_url=url.url,
            user=user,
            url_service=url.service,
        )
        await interaction.response.send_message(content)

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Find a new video that's horror game related.", name="find_horror")
    async def find_horor(
        self,
        interaction: discord.Interaction,
        user: typing.Optional[typing.Union[discord.Member, discord.User]],
        service: typing.Optional[str],
    ):

        content_type = ContentType.horror
        result = await database_lookup(self.bot, content_type, user, service)
        user = result.user or "Unknown"
        await interaction.response.send_message(content=f"Video: {result.url}\nService: {result.service}\nAdded By: {user} \n{result.name} {result.value}")

    @find_horror.autocomplete("service")
    async def find_horror_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM content where content_type = $1", ContentType.horror.value)

        all_choices = [Choice(name=service.service, value=service.service) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith[0:25]

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Gets a random video game video from the database", name="quick_games")
    async def quick_games(self, interaction: discord.Interaction):

        url = await self.bot.db.fetchrow("SELECT user_id, url, service from content where content_type = $1 ORDER BY RANDOM()", ContentType.games.value)
        user = await self.bot.try_user(url.user_id)
        content = await self.bot.tree.translator.translate_content(
            interaction,
            "Video: {url_url}\nAdded by {user}\nService: {url_service}",
            url_url=url.url,
            user=user,
            url_service=url.service,
        )
        await interaction.response.send_message(content)

    @app_commands.user_install()
    @app_commands.guild_install()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(description="Find a new video that's video game related.", name="find_games")
    async def find_games(
        self,
        interaction: discord.Interaction,
        user: typing.Optional[typing.Union[discord.Member, discord.User]],
        service: typing.Optional[str],
    ):

        content_type = ContentType.games
        result = await database_lookup(self.bot, content_type, user, service)
        user = result.user or "Unknown"
        await interaction.response.send_message(content=f"Video: {result.url}\nService: {result.service}\nAdded By: {user} \n{result.name} {result.value}")

    @find_horror.autocomplete("service")
    async def find_games_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM content where content_type = $1", ContentType.gamesvalue)

        all_choices = [Choice(name=service.service, value=service.service) for service in services]
        startswith = [choices for choices in all_choices if choices.name.startswith(current)]
        if not (current and startswith):
            return all_choices[0:25]

        return startswith[0:25]


async def setup(bot):
    await bot.add_cog(Find(bot))
