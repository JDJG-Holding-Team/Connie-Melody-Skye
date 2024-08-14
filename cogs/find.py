from __future__ import annotations

import random
import traceback
import typing

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from utils.extra import ContentType

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
        content_type = ContentType.music.value
        if user and not service:
            user_id = user.id
            proper_urls = await self.bot.db.fetch("SELECT user_id, url, service FROM CONTENT WHERE user_id = $1 and content_type = $2", user_id, content_type)
            if not proper_urls:
                proper_urls = await self.bot.db.fetch("SELECT user_id, url, service FROM CONTENT where content_type = $1", content_type)

            url = random.choice(proper_urls)
            user = await self.bot.try_user(url.user_id)
            name = "User Songs"
            value = f"\U0001f3a7"

        elif service and not user:
            proper_urls = await self.bot.db.fetch("SELECT user_id, url, service FROM CONTENT WHERE service = $1 and content_type = $2", service, content_type)
            url = random.choice(proper_urls)

            name = "Service Songs"
            value = f"\U0001f5a5"

            user = await self.bot.try_user(url.user_id)

        elif service and user:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT user_id, url, service FROM CONTENT WHERE service = $1 and user_id = $2 and content_type = $3", service, user_id, content_type)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT user_id, url, service FROM CONTENT WHERE service = $1 and content_type = $2", service, content_type)

                if not proper_urls:

                    proper_urls = await self.bot.db.fetch("SELECT user_id, url, service from content where content_type = $1", content_type)

            url = random.choice(proper_urls)

            user = await self.bot.try_user(url.user_id)

            name = "User and Service Songs"
            value = f"\U0001f3a7 \U0001f5a5"

        else:
            proper_urls = await self.bot.db.fetch("SELECT user_id, url, service FROM CONTENT where content_type = $1", content_type)

            url = random.choice(proper_urls)

            name = "Randomly Chosen"
            value = "\U0001f570"

            user = await self.bot.try_user(url.user_id)

        if not user:
            user = "Unknown"

        # this definetly needs cleanup
        await interaction.response.send_message(content=f"Song: {url.url}\nService: {url.service}\nAdded By: {user} \n{name} {value}")

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

        if user and not service:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT * from misc_videos WHERE user_id = $1", user_id)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT * from misc_videos")

            url = random.choice(proper_urls)

            user = await self.bot.try_user(url.user_id)

            name = "User Videos"
            value = f"\U0001f4fa"

        elif service and not user:
            proper_urls = await self.bot.db.fetch("SELECT * from misc_videos WHERE service = $1", service)
            url = random.choice(proper_urls)

            name = "Service Videos"
            value = f"\U0001f5a5"

            user = await self.bot.try_user(url.user_id)

        elif service and user:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT * from misc_videos WHERE service = $1 and user_id = $2", service, user_id)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT * from misc_videos WHERE service = $1", service)

                if not proper_urls:

                    proper_urls = await self.bot.db.fetch("SELECT * from misc_videos")

            url = random.choice(proper_urls)

            user = await self.bot.try_user(url.user_id)

            name = "User and Service Videos"
            value = f"\U0001f4fa \U0001f5a5"

        else:
            proper_urls = await self.bot.db.fetch("SELECT * from misc_videos")

            url = random.choice(proper_urls)

            name = "Randomly Chosen"
            value = "\U0001f570"

            user = await self.bot.try_user(url.user_id)

        if not user:
            user = "Unknown"

        # this definetly needs cleanup
        await interaction.response.send_message(content=f"Video: {url.url}\nService: {url.service}\nAdded By: {user} \n{name} {value}")
       

    @find_misc.autocomplete("service")
    async def find_misc_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM misc_videos")

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

        if user and not service:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT * from tech_videos WHERE user_id = $1", user_id)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT * from tech_videos")

            url = random.choice(proper_urls)

            user = await self.bot.try_user(url.user_id)

            name = "User Videos"
            value = f"\U0001f4fa"

        elif service and not user:
            proper_urls = await self.bot.db.fetch("SELECT * from tech_videos WHERE service = $1", service)
            url = random.choice(proper_urls)

            name = "Service Videos"
            value = f"\U0001f5a5"

            user = await self.bot.try_user(url.user_id)

        elif service and user:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT * from tech_videos WHERE service = $1 and user_id = $2", service, user_id)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT * from tech_videos WHERE service = $1", service)

                if not proper_urls:

                    proper_urls = await self.bot.db.fetch("SELECT * from tech_videos")

            url = random.choice(proper_urls)

            user = await self.bot.try_user(url.user_id)

            name = "User and Service Videos"
            value = f"\U0001f4fa \U0001f5a5"

        else:
            proper_urls = await self.bot.db.fetch("SELECT * from tech_videos")

            url = random.choice(proper_urls)

            name = "Randomly Chosen"
            value = "\U0001f570"

            user = await self.bot.try_user(url.user_id)

        if not user:
            user = "Unknown"

        # this definetly needs cleanup
        await interaction.response.send_message(content=f"Video: {url.url}\nService: {url.service}\nAdded By: {user} \n{name} {value}")

    @find_tech.autocomplete("service")
    async def find_tech_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM tech_videos")

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

        if user and not service:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT * from watched_videos WHERE user_id = $1", user_id)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT * from watched_videos")

            url = random.choice(proper_urls)

            user = await self.bot.try_user(url.user_id)

            name = "User Videos"
            value = f"\U0001f4fa"

        elif service and not user:
            proper_urls = await self.bot.db.fetch("SELECT * from watched_videos WHERE service = $1", service)
            url = random.choice(proper_urls)

            name = "Service Videos"
            value = f"\U0001f5a5"

            user = await self.bot.try_user(url.user_id)

        elif service and user:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT * from watched_videos WHERE service = $1 and user_id = $2", service, user_id)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT * from watched_videos WHERE service = $1", service)

                if not proper_urls:

                    proper_urls = await self.bot.db.fetch("SELECT * from watched_videos")

            url = random.choice(proper_urls)

            user = await self.bot.try_user(url.user_id)

            name = "User and Service Videos"
            value = f"\U0001f4fa \U0001f5a5"

        else:
            proper_urls = await self.bot.db.fetch("SELECT * from watched_videos")

            url = random.choice(proper_urls)

            name = "Randomly Chosen"
            value = "\U0001f570"

            user = await self.bot.try_user(url.user_id)

        if not user:
            user = "Unknown"
        
        # this definetly needs cleanup
        await interaction.response.send_message(content=f"Video: {url.url}\nService: {url.service}\nAdded By: {user} \n{name} {value}")
        

    @find_watched.autocomplete("service")
    async def find_watched_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM watched_videos")

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

        if user and not service:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT * from to_watch WHERE user_id = $1", user_id)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT * from to_watch")

            url = random.choice(proper_urls)

            user = await self.bot.try_user(url.user_id)

            name = "User Videos"
            value = f"\U0001f4fa"

        elif service and not user:
            proper_urls = await self.bot.db.fetch("SELECT * from to_watch WHERE service = $1", service)
            url = random.choice(proper_urls)

            name = "Service Videos"
            value = f"\U0001f5a5"

            user = await self.bot.try_user(url.user_id)

        elif service and user:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT * from to_watch WHERE service = $1 and user_id = $2", service, user_id)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT * from to_watch WHERE service = $1", service)

                if not proper_urls:

                    proper_urls = await self.bot.db.fetch("SELECT * from to_watch")

            url = random.choice(proper_urls)

            user = await self.bot.try_user(url.user_id)

            name = "User and Service Videos"
            value = f"\U0001f4fa \U0001f5a5"

        else:
            proper_urls = await self.bot.db.fetch("SELECT * from to_watch")

            url = random.choice(proper_urls)

            name = "Randomly Chosen"
            value = "\U0001f570"

            user = await self.bot.try_user(url.user_id)

        if not user:
            user = "Unknown"

        # this definetly needs cleanup
        await interaction.response.send_message(content=f"Video: {url.url}\nService: {url.service}\nAdded By: {user} \n{name} {value}")
      

    @find_to_watch.autocomplete("service")
    async def find_watched_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM to_watch")

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

        proper_urls = await self.bot.db.fetch("SELECT user_id, url, service from content where content_type = $1", ContentType.music.value)

        url = random.choice(proper_urls)

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

        proper_urls = await self.bot.db.fetch("SELECT * from watched_videos")
        url = random.choice(proper_urls)

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

        proper_urls = await self.bot.db.fetch("SELECT * from to_watch")

        url = random.choice(proper_urls)
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

        proper_urls = await self.bot.db.fetch("SELECT * from misc_videos")

        url = random.choice(proper_urls)
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

        proper_urls = await self.bot.db.fetch("SELECT * from tech_videos")

        url = random.choice(proper_urls)
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

        proper_urls = await self.bot.db.fetch("SELECT * from anime_videos")

        url = random.choice(proper_urls)
        user = await self.bot.try_user(url.user_id)
        content = await self.bot.tree.translator.translate_content(
            interaction,
            "Video: {url_url}\nAdded by {user}\nService: {url_service}",
            url_url=url.url,
            user=user,
            url_service=url.service,
        )
        await interaction.response.send_message(content)

    # make spanish and japanese translations
    # ask volunteers if they can help me with this.

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

        # no describe for autocomplete args?

        if user and not service:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT * from anime_videos WHERE user_id = $1", user_id)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT * from anime_videos")

            url = random.choice(proper_urls)

            user = await self.bot.try_user(url.user_id)

            name = "User Videos"
            value = f"\U0001f4fa"

        elif service and not user:
            proper_urls = await self.bot.db.fetch("SELECT * from anime_videos WHERE service = $1", service)
            url = random.choice(proper_urls)

            name = "Service Videos"
            value = f"\U0001f5a5"

            user = await self.bot.try_user(url.user_id)

        elif service and user:

            user_id = user.id

            proper_urls = await self.bot.db.fetch("SELECT * from anime_videos WHERE service = $1 and user_id = $2", service, user_id)

            if not proper_urls:

                proper_urls = await self.bot.db.fetch("SELECT * from anime_videos WHERE service = $1", service)

                if not proper_urls:

                    proper_urls = await self.bot.db.fetch("SELECT * from anime_videos")

            url = random.choice(proper_urls)

            user = await self.bot.try_user(url.user_id)

            name = "User and Service Videos"
            value = f"\U0001f4fa \U0001f5a5"

        else:
            proper_urls = await self.bot.db.fetch("SELECT * from anime_videos")

            url = random.choice(proper_urls)

            name = "Randomly Chosen"
            value = "\U0001f570"

            user = await self.bot.try_user(url.user_id)

        if not user:
            user = "Unknown"
        
        # this definetly needs cleanup
        await interaction.response.send_message(f"Video: {url.url}\nService: {url.service}\nAdded By: {user} \n{name} {value}")
      

    @find_anime.autocomplete("service")
    async def find_anime_autocomplete(self, interaction: discord.Interaction, current: str):

        services = await self.bot.db.fetch("SELECT DISTINCT service FROM anime_videos")

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
                label=f"Source",
                url=url,
                style=discord.ButtonStyle.link,
            )
        )
        await interaction.response.send_message(f"Source: {url}", view=view)


async def setup(bot):
    await bot.add_cog(Find(bot))
