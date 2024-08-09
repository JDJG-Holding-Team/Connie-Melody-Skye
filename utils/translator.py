from __future__ import annotations

import pathlib
import random
from typing import TYPE_CHECKING, Any, NotRequired, TypedDict

try:
    import orjson as json
except ImportError:
    import json

import discord
from discord import app_commands
from discord.app_commands import TranslationContextLocation, TranslationContextTypes, locale_str

if TYPE_CHECKING:
    from main import ConnieSkye


class LocaleCommandEmbedAuthor(TypedDict):
    name: str | None


class LocaleCommandEmbedFooter(TypedDict):
    text: str | None


class LocaleComamndEmbedField(TypedDict):
    name: str | None
    value: str | None


class LocaleCommandEmbed(TypedDict):
    title: NotRequired[str | None]
    description: NotRequired[str | None]
    fields: NotRequired[list[LocaleComamndEmbedField]]
    footer: NotRequired[LocaleCommandEmbedFooter]
    author: NotRequired[LocaleCommandEmbedAuthor]


class LocaleCommandOption(TypedDict):
    name: str | None
    description: NotRequired[str | None]
    choices: NotRequired[list[str]]


class LocaleCommand(TypedDict):
    name: str | None
    description: NotRequired[str | None]
    options: NotRequired[dict[str, LocaleCommandOption]]
    embeds: NotRequired[list[LocaleCommandEmbed]]
    content: NotRequired[str | None]
    translator_id: str


# for type hinting the translator
class TreeWithTranslator(app_commands.CommandTree):
    translator: TreeTranslator  # type: ignore


class TreeTranslator(app_commands.Translator):
    LOCALS_PATH = "./locales"
    # dynamically loaded in load
    LOCALE_TO_FILE: dict[discord.Locale, str] = {}
    EXCLUDE_LOCALES: list[discord.Locale] = []

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # locale: {command_name: LocaleCommand}
        self.cached_locales: dict[discord.Locale, dict[str, LocaleCommand]] = {}

    async def load(self) -> None:
        locale_directory = pathlib.Path(self.LOCALS_PATH)
        files = list(locale_directory.rglob("*.json"))

        for file in files:
            try:
                locale = discord.Locale(file.stem)
            except ValueError:
                raise ValueError(f"Invalid locale file {file.name}. Expected a file like `en-US.json`.")
                # I should tell soheab to tell the user that it will use the english us locale as a default because that way it still functions.

            if locale in self.EXCLUDE_LOCALES:
                continue

            self.LOCALE_TO_FILE[locale] = file.name
            await self.get_locale(locale)

    async def unload(self) -> None:
        self.cached_locales.clear()
        self.LOCALE_TO_FILE.clear()

    def _ensure_translator_id(self, locale: discord.Locale, data: dict[str, LocaleCommand]) -> None:
        for command in data.values():
            if "translator_id" not in command:
                raise ValueError(
                    (
                        f'Missing translator_id for command "{command["name"]}"'
                        f" in locale file {self.LOCALE_TO_FILE[locale]}. Please add it."
                    )
                )

    async def get_locale(
        self,
        locale: discord.Locale,
    ) -> dict[str, LocaleCommand]:
        if locale in self.cached_locales:
            return self.cached_locales[locale]

        file = self.LOCALE_TO_FILE[locale]
        with open(f"{self.LOCALS_PATH}/{file}", encoding="UTF-8") as f:
            data = json.loads(f.read())
            self._ensure_translator_id(locale, data)
            self.cached_locales[locale] = data

        return data

    async def get_command(self, locale: discord.Locale, command_name: str) -> LocaleCommand | None:
        locales = await self.get_locale(locale)
        return locales.get(command_name)

    async def _get_translator(
        self, interaction: discord.Interaction[ConnieSkye]
    ) -> discord.User | None:
        command = await self.get_command(interaction.locale, interaction.command.qualified_name)  # type: ignore
        if not command:
            raise ValueError(f"Command {interaction.command.qualified_name} not found in locale {interaction.locale}.")  # type: ignore

        translator_id = command.get("translator_id")
        return await interaction.client.try_user(int(translator_id))

    async def translate_embeds(
        self,
        interaction: discord.Interaction[ConnieSkye],
        embeds: list[discord.Embed],
        **string_formats: Any,
    ) -> list[discord.Embed]:
        new_embeds: list[discord.Embed] = []

        async def do_translate(value: str | None, key: str) -> str | None:
            if not value:
                return None

            translated = await interaction.translate(locale_str(value, key=key), data=interaction.command)
            return (translated or value).format(**string_formats)

        for idx, embed in enumerate(embeds):
            embed = embed.copy()
            embed.title = await do_translate(embed.title, f"embed:{idx}:title")
            embed.description = await do_translate(embed.description, f"embed:{idx}:description")

            embed.set_footer(
                text=await do_translate(embed.footer.text, f"embed:{idx}:footer"), icon_url=embed.footer.icon_url
            )

            author_name = await do_translate(embed.author.name, f"embed:{idx}:author")
            if random.randint(0, 4) == 4:
                translator = await self._get_translator(interaction)
                if translator:
                    author_name = f"{f'{author_name} | ' if author_name else ''}Translated by {translator}"

            embed.set_author(
                name=author_name,
                icon_url=embed.author.icon_url,
            )
            if not any((author_name, embed.author.icon_url)):
                embed.remove_author()

            for field_idx, field in enumerate(embed.fields.copy()):
                field.name = await do_translate(field.name, f"embed:{idx}:fields:{field_idx}:name")
                field.value = await do_translate(field.value, f"embed:{idx}:fields:{field_idx}:value")
                embed.set_field_at(field_idx, name=field.name, value=field.value, inline=field.inline)

            new_embeds.append(embed)

        return new_embeds

    async def translate_choice_name(
        self,
        locale: discord.Locale,
        command: str | LocaleCommand,
        option_name: str,
        index: int,
    ) -> str | None:
        _command = await self.get_command(locale, command) if not isinstance(command, dict) else command
        if not _command:
            return None

        choices = _command.get("options", {}).get(option_name, {}).get("choices")
        if not choices:
            return None

        return choices[index]

    async def translate_choice_name_from_locale_key(
        self,
        locale: discord.Locale,
        locale_key: locale_str | None,
    ) -> str | None:
        if not locale_key:
            return None

        if not locale_key.extras or "key" not in locale_key.extras:
            raise ValueError(
                "Choice name requires you to pass the key in extras. Like `locale_str('key', key='command name:option name:index')`"
            )

        try:
            command_name, option_name, idx = locale_key.extras["key"].split(":")
        except ValueError:
            raise ValueError(
                "Choice name requires you to pass the key in extras. Like `locale_str('key', key='command name:option name:index')`"
            )

        idx = int(idx)
        command = await self.get_command(locale, command_name)
        if not command:
            return None

        return await self.translate_choice_name(locale, command, option_name, idx)

    async def translate_content(self, interaction: discord.Interaction, content: str, **string_formats: Any) -> str:
        translated = await interaction.translate(locale_str(content, key="content"), data=interaction.command)
        return (translated or content).format(**string_formats)

    async def translate(
        self, string: app_commands.locale_str, locale: discord.Locale, context: TranslationContextTypes
    ) -> str | None:
        if locale not in self.LOCALE_TO_FILE or locale in self.EXCLUDE_LOCALES:
            return None

        command_name: str | None = None

        if context.data:
            if isinstance(
                context.data,
                (discord.app_commands.Command, discord.app_commands.ContextMenu, discord.app_commands.Group),
            ):
                command_name = context.data.qualified_name
            elif isinstance(context.data, discord.app_commands.Parameter):
                command_name = context.data.command.qualified_name

        if context.location is TranslationContextLocation.choice_name:
            extras = string.extras
            if "key" in extras:
                try:
                    command_name, option_name, idx = extras["key"].split(":")
                except ValueError:
                    raise ValueError(
                        "Choice name requires you to pass the key in extras. Like `locale_str('key', key='command name:option name:index')`"
                    )

                string.extras["index"] = int(idx)
                string.extras["option"] = option_name

        command_name = string.extras.get("command") or command_name

        if not command_name:
            raise ValueError(
                (
                    f"locale_str for location {context.location} requires you to pass the"
                    f"command name in extras. Like `locale_str('key', command='command name')`"
                    " or a command/parameter as context.data."
                )
            )

        if context.location is TranslationContextLocation.other:
            key = string.extras.get("key")  # type: ignore
            if not key:
                raise ValueError

        if not command_name:
            raise ValueError("Command name is not provided. Expected a command name in context.data or extras.")

        command = await self.get_command(locale, command_name)
        if not command:
            return None

        if context.location is TranslationContextLocation.command_name:
            return command.get("name")

        elif context.location in (
            TranslationContextLocation.command_description,
            TranslationContextLocation.group_description,
        ):
            return command.get("description")

        elif context.location in (
            TranslationContextLocation.parameter_name,
            TranslationContextLocation.parameter_description,
        ):
            _, key = context.location.name.split("_")
            return command.get("options", {}).get(context.data.name, {}).get(key)

        elif context.location is TranslationContextLocation.choice_name:
            idx = string.extras.get("index")
            if idx is None:
                raise ValueError(
                    "Choice name requires you to pass the index in extras. Like `locale_str('key', index=0)`"
                )

            option_name = string.extras.get("option")
            if not option_name:
                raise ValueError(
                    "Choice name requires you to pass the option name in extras. Like `locale_str('key', option='option')`"
                )
            return await self.translate_choice_name(locale, command, option_name, idx)

        elif context.location is TranslationContextLocation.other:
            key: str = string.extras.get("key") or ""
            if not key:
                raise ValueError(
                    "locale_str for location other requires you to pass the type in extras. Like `locale_str('string', key='type')`"
                )

            if key.startswith("embed"):
                try:
                    _, idx, field, *fields_extra = key.split(":")
                except ValueError:
                    raise ValueError(
                        f"Invalid type for embed. Expected `embed:<index>:<field>`. Got {key}. Example: `embed:0:title`."
                    )

                idx = int(idx)
                field = field.lower()
                embed = command.get("embeds", [{}])[idx]
                if not embed:
                    return None

                if field == "title":
                    return embed.get("title")
                elif field == "description":
                    return embed.get("description")
                elif field == "footer":
                    return embed.get("footer", {}).get("text")
                elif field == "author":
                    return embed.get("author", {}).get("name")
                elif field == "fields":
                    if not fields_extra:
                        raise ValueError(
                            f"Invalid type for embed. Expected `embed:<index>:fields:<field_index>:name`. Got {key}. Example: `embed:0:fields:0:name`."
                        )

                    try:
                        field_idx, field_type = fields_extra
                    except ValueError:
                        raise ValueError(
                            f"Invalid type for embed. Expected `embed:<index>:fields:<field_index>:name`. Got {key}. Example: `embed:0:fields:0:name`."
                        )

                    field_idx = int(field_idx)

                    field = embed.get("fields", [{}])[field_idx]
                    if not field:
                        return None

                    if field_type == "name":
                        return field.get("name")
                    elif field_type == "value":
                        return field.get("value")
                    else:
                        raise ValueError(f"Field type {field_type} is not valid. Expected `name` or `value`.")

                else:
                    raise ValueError(
                        f"Field {field} is not valid. Expected `title`, `description`, `footer`, `author` or `fields`."
                    )

            elif key == "content":
                return command.get("content")

        else:
            return None
