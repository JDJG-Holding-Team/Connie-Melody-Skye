import traceback
import typing


from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(brief="Adds to music videos")
    async def add_music(self, ctx, url: typing.Optional[str] = None):

        url = await self.bot.db.fetchrow("SELECT * from music where url = $1", url)
        if url:
            return await ctx.send(f"{url} already in music videos.")

        return await ctx.send(f"{url} added to music.")

    @commands.command(brief="Adds to watched_videos videos")
    async def add_watched_videos(self, ctx, url: typing.Optional[str] = None):

        url = await self.bot.db.fetchrow("SELECT * from watched_videos where url = $1", url)
        if url:
            return await ctx.send(f"{url} already in watched_videos videos.")

        return await ctx.send(f"{url} added to watched_videos")

    @commands.command(brief="Adds to watched_videos videos")
    async def add_watched_videos(self, ctx, url: typing.Optional[str] = None):

        url = await self.bot.db.fetchrow("SELECT * from watched_videos where url = $1", url)
        if url:
            return await ctx.send(f"{url} already in watched_videos videos.")

        return await ctx.send(f"{url} added to watched_videos")

    @commands.command(brief="Adds to to_watch videos")
    async def add_to_watch(self, ctx, url: typing.Optional[str] = None):

        url = await self.bot.db.fetchrow("SELECT * from to_watch where url = $1", url)
        if url:
            return await ctx.send(f"{url} already in to_watch videos.")

        return await ctx.send(f"{url} added to to_watch")

    @commands.command(brief="Adds idk videos")
    async def add_idk(self, ctx, url: typing.Optional[str] = None):

        url = await self.bot.db.fetchrow("SELECT * from idk_videos where url = $1", url)
        if url:
            return await ctx.send(f"{url} already in idk_videos.")

        return await ctx.send(f"{url} added to idk_videos")
    
    
    async def cog_command_error(self, ctx, error):
        await ctx.send(error)
        traceback.print_exc(error)

    # error stuff lol

    # idk about remove stuff so idk.


async def setup(bot):
    await bot.add_cog(Owner(bot))
