import traceback
import typing

import discord
from discord.ext import commands

from utils.extra import ContentType

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_text = "Url cannot be None"

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(brief="Adds to music videos")
    async def add_music(self, ctx, url: typing.Optional[str] = None, user : typing.Optional[discord.User] = commands.Author, *, service : typing.Optional[str] = None):
        
        content_type = ContentType.music
        service = service or "YouTube"

        if not url:
            return await ctx.send("Url must exist, it cannot be None.")

        url_check = await self.bot.db.fetchrow("SELECT user_id, url, service FROM CONTENT where url = $1 and content_type = $2", url, content_type.value)
        if url_check:
            return await ctx.send(f"{url} already in {content_type.name} videos.")

        await self.bot.db.execute("INSERT INTO content VALUES($1, $2, $3, $4)", user.id, url, service, content_type.value)
        return await ctx.send(f"{url} added to {content_type.name}.")
    
    @commands.command(brief="Removes music videos")
    async def remove_music(self, ctx, url: typing.Optional[str] = None):

        content_type = ContentType.music
        if not url:
            return await ctx.send(self.error_text)
        
        url_check = await self.bot.db.fetchrow("SELECT user_id, url, service FROM CONTENT where url = $1 and content_type = $2", url, content_type.value)

        if not url_check:
            return await ctx.send(f"{url} must be in database")
        
        await self.bot.db.execute("DELETE FROM CONTENT WHERE url = $1 and content_Type = $2", url, content_type.value)
        return await ctx.send(f"Removed {url} from database ({content_type.name})")

    @commands.command(brief="Adds to watched_videos videos")
    async def add_watched_videos(self, ctx, url: typing.Optional[str] = None, user : typing.Optional[discord.User] = commands.Author, *, service : typing.Optional[str] = None):
        
        content_type = ContentType.watched
        service = service or "YouTube"

        if not url:
            return await ctx.send("Url must exist, it cannot be None.")

        url_check = await self.bot.db.fetchrow("SELECT user_id, url, service FROM CONTENT where url = $1 and content_type = $2", url, content_type.value)
        if url_check:
            return await ctx.send(f"{url} already in {content_type.name} videos.")

        await self.bot.db.execute("INSERT INTO content VALUES($1, $2, $3, $4)", user.id, url, service, content_type.value)
        return await ctx.send(f"{url} added to {content_type.name} videos.")
    
    @commands.command(brief="Removes watched videos")
    async def remove_watched_videos(self, ctx, url: typing.Optional[str] = None):

        content_type = ContentType.watched
        if not url:
            return await ctx.send(self.error_text)
        
        url_check = await self.bot.db.fetchrow("SELECT user_id, url, service FROM CONTENT where url = $1 and content_type = $2", url, content_type.value)

        if not url_check:
            return await ctx.send(f"{url} must be in database")
        
        await self.bot.db.execute("DELETE FROM CONTENT WHERE url = $1 and content_Type = $2", url, content_type.value)
        return await ctx.send(f"Removed {url} from database ({content_type.name})")

    @commands.command(brief="Adds to to_watch videos")
    async def add_to_watch(self, ctx, url: typing.Optional[str] = None, user : typing.Optional[discord.User] = commands.Author, *, service : typing.Optional[str] = None):

        service = service or "YouTube"

        if not url:
            return await ctx.send("Url must exist, it cannot be None.")

        url_check = await self.bot.db.fetchrow("SELECT * from to_watch where url = $1", url)
        if url_check:
            return await ctx.send(f"{url} already in to_watch videos.")

        await self.bot.db.execute("INSERT INTO to_watch VALUES($1, $2, $3)", user.id, url, service)
        return await ctx.send(f"{url} added to database (to_watch).")

    @commands.command(brief="Removes to_watch videos")
    async def remove_to_watch(self, ctx, url: typing.Optional[str] = None):
        if not url:
            return await ctx.send(self.error_text)
        
        url_check = await self.bot.db.fetchrow("SELECT * from to_watch where url = $1", url)

        if not url_check:
            return await ctx.send(f"{url} must be in database")
        
        await self.bot.db.execute("DELETE FROM to_watch WHERE url = $1", url)
        return await ctx.send(f"Removed {url} from database (to_watch)")

    @commands.command(brief="Adds misc videos")
    async def add_misc(self, ctx, url: typing.Optional[str] = None, user : typing.Optional[discord.User] = commands.Author, *, service : typing.Optional[str] = None):

        content_type = ContentType.misc
        service = service or "YouTube"

        if not url:
            return await ctx.send("Url must exist, it cannot be None.")

        url_check = await self.bot.db.fetchrow("SELECT user_id, url, service FROM CONTENT where url = $1 and content_type = $2", url, content_type.value)
        if url_check:
            return await ctx.send(f"{url} already in {content_type.name} videos.")

        await self.bot.db.execute("INSERT INTO content VALUES($1, $2, $3, $4)", user.id, url, service, content_type.value)
        return await ctx.send(f"{url} added to {content_type.name} videos.")

    @commands.command(brief="Removes misc videos")
    async def remove_misc_videos(self, ctx, url: typing.Optional[str] = None):

        content_type = ContentType.misc
        if not url:
            return await ctx.send(self.error_text)
        
        url_check = await self.bot.db.fetchrow("SELECT user_id, url, service FROM CONTENT where url = $1 and content_type = $2", url, content_type.value)

        if not url_check:
            return await ctx.send(f"{url} must be in database")
        
        await self.bot.db.execute("DELETE FROM CONTENT WHERE url = $1 and content_Type = $2", url, content_type.value)
        return await ctx.send(f"Removed {url} from database ({content_type.name})")
        
    
    @commands.command(brief="Adds Tech videos")
    async def add_tech(self, ctx, url: typing.Optional[str] = None, user : typing.Optional[discord.User] = commands.Author, *, service : typing.Optional[str] = None):

        service = service or "YouTube"

        if not url:
            return await ctx.send("Url must exist, it cannot be None.")

        url_check = await self.bot.db.fetchrow("SELECT * from tech_videos where url = $1", url)
        if url_check:
            return await ctx.send(f"{url} already in tech_videos.")

        await self.bot.db.execute("INSERT INTO tech_videos VALUES($1, $2, $3)", user.id, url, service)
        return await ctx.send(f"{url} added to tech_videos")
    
    @commands.command(brief="Removes Tech videos")
    async def remove_tech_videos(self, ctx, url: typing.Optional[str] = None):
        if not url:
            return await ctx.send(self.error_text)
        
        url_check = await self.bot.db.fetchrow("SELECT * from tech_videos where url = $1", url)

        if not url_check:
            return await ctx.send(f"{url} must be in database")
        
        await self.bot.db.execute("DELETE FROM tech_videos WHERE url = $1", url)
        return await ctx.send(f"Removed {url} from database (tech_videos)")

    @commands.command(brief="Adds anime videos")
    async def add_anime(self, ctx, url: typing.Optional[str] = None, user : typing.Optional[discord.User] = commands.Author, *, service : typing.Optional[str] = None):
        
        service = service or "YouTube"

        if not url:
            return await ctx.send("Url must exist, it cannot be None.")

        url_check = await self.bot.db.fetchrow("SELECT * from anime_videos where url = $1", url)
        if url_check:
            return await ctx.send(f"{url} already in anime_videos.")

        await self.bot.db.execute("INSERT INTO anime_videos VALUES($1, $2, $3)", user.id, url, service)
        return await ctx.send(f"{url} added to anime_videos")

    @commands.command(brief="Removes anime videos")
    async def remove_anime_videos(self, ctx, url: typing.Optional[str] = None):
        if not url:
            return await ctx.send(self.error_text)
        
        url_check = await self.bot.db.fetchrow("SELECT * from anime_videos where url = $1", url)

        if not url_check:
            return await ctx.send(f"{url} must be in database")
        
        await self.bot.db.execute("DELETE FROM anime_videos WHERE url = $1", url)
        return await ctx.send(f"Removed {url} from database (anime_videos)")
    
    
    async def cog_command_error(self, ctx, error):
        await ctx.send(error)
        traceback.print_exc(error)

    # error stuff lol

    # idk about remove stuff so idk.
        
    # good everything good here.


async def setup(bot):
    await bot.add_cog(Owner(bot))
