import discord
from discord.ext import commands
from discord import ButtonStyle, SelectOption
from discord.ui import Button, Select, View

class Dropdown(discord.ui.Select):
    def __init__(self, options, bot):
        self.bot = bot
        super().__init__(placeholder="Select a category", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        label = self.values[0]
        for cog in self.bot.cogs:
            if label == cog:
                await get_help(self, interaction, CogToPassAlong=cog)
                return
        if label == "Close":
            embede = discord.Embed(
                title=":books: Help System",
                description=f"Welcome To {self.bot.user.name} Help System",
            )
            embede.set_footer(text="Use dropdown to select category")
            await interaction.response.edit_message(embed=embede, view=None)


class DropdownView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        options = [SelectOption(label=cog, value=cog) for cog in bot.cogs]
        options.append(SelectOption(label="Close", value="Close"))
        self.add_item(Dropdown(options, self.bot))

class PaginationView(discord.ui.View):
    def __init__(self, embeds, bot):
        super().__init__()
        self.embeds = embeds
        self.current_page = 0
        self.bot = bot
        self.add_item(Dropdown([SelectOption(label=cog, value=cog) for cog in bot.cogs] + [SelectOption(label="Close", value="Close")], self.bot))
        self.add_item(Button(style=ButtonStyle.primary, label="◀", custom_id="previous"))
        self.add_item(Button(style=ButtonStyle.primary, label="▶", custom_id="next"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.data["custom_id"] == "previous":
            self.current_page = max(0, self.current_page - 1)
        elif interaction.data["custom_id"] == "next":
            self.current_page = min(len(self.embeds) - 1, self.current_page + 1)

        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)
        return True

class Help(commands.Cog):
    "The Help Menu Cog"
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="Shows the help menu")
    async def help_slash(self, inter: discord.Interaction, command: str = None):
        await self.handle_help(inter, command)

    @commands.command(name="help")
    async def help_command(self, ctx, *, command=None):
        await self.handle_help(ctx, command)

    async def handle_help(self, invoke_obj, command=None):
        if command is None:
            await self.send_bot_help(invoke_obj)
        else:
            cmd = self.bot.get_command(command)
            if cmd:
                await self.send_command_help(invoke_obj, cmd)
            else:
                await invoke_obj.response.send_message(
                    f"No command called '{command}' found.", ephemeral=True
                )

    async def send_bot_help(self, invoke_obj):
        embede = discord.Embed(
            title=":books: Help System",
            description=f"Welcome To {self.bot.user.name} Help System",
        )
        embede.set_footer(text="Use dropdown to select category")
        view = DropdownView(self.bot)
        await invoke_obj.response.send_message(embed=embede, view=view)

    async def send_command_help(self, invoke_obj, command):
        signature = f"/{command.name}" if isinstance(invoke_obj, discord.Interaction) else f"{invoke_obj.prefix}{command.name}"
        if isinstance(command, commands.Command):
            signature += f" {command.signature}"
        embed = HelpEmbed(
            title=signature, description=command.help or "No help found..."
        )

        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        embed.add_field(name="Usable", value="Yes")

        if command._buckets and (cooldown := command._buckets._cooldown):
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
            )

        await invoke_obj.response.send_message(embed=embed)

class HelpEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = discord.utils.utcnow()
        self.set_footer(text="Use dropdown to select category")

async def get_help(self, interaction, CogToPassAlong):
    cog = self.bot.get_cog(CogToPassAlong)
    if not cog:
        return
    embeds = []
    embed = discord.Embed(
        title=f"{CogToPassAlong} - Commands",
        description=cog.__doc__,
    )
    embed.set_author(name="Help System")
    commands_text = ""
    for command in cog.get_commands():
        if isinstance(command, commands.Command):
            command_text = f"『`{command.name}`』: {command.help}\n"
            if len(commands_text) + len(command_text) > 1024:
                embed.add_field(name="Commands", value=commands_text, inline=False)
                embeds.append(embed)
                embed = discord.Embed(
                    title=f"{CogToPassAlong} - Commands (Continued)",
                    description=cog.__doc__,
                )
                embed.set_author(name="Help System")
                commands_text = command_text
            else:
                commands_text += command_text
    if commands_text:
        embed.add_field(name="Commands", value=commands_text, inline=False)
    embeds.append(embed)

    if len(embeds) > 1:
        view = PaginationView(embeds, self.bot)
        await interaction.response.edit_message(embed=embeds[0], view=view)
    else:
        await interaction.response.edit_message(embed=embeds[0])

def setup(bot):
    bot.add_cog(Help(bot))
