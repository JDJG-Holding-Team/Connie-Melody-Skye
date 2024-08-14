from __future__ import annotations

import enum
import typing

from typing import NamedTuple

import discord

if typing.TYPE_CHECKING:
    from main import ConnieSkye

class ContentType(enum.IntEnum):
    music = 0
    tech = 1
    anime = 2
    misc = 3
    watch = 4
    watched = 5

class DatabaseData(NamedTuple):
    url: str
    service: str
    user: typing.Optional[discord.User]
    name: str
    value: str

    def __str__(self) -> str:
        return self.url

async def database_lookup(bot: ConnieSkye, content_type: ContentType, user : typing.Optional[discord.User], service: typing.Optional[str] = None):

    result = None
    name = None
    value = None

    if user and not service:
        user_id = user.id
        result = await bot.db.fetchrow("SELECT user, url, service FROM CONTENT WHERE user_id = $1 and content_type = $2 ORDER BY RANDOM()", user_id, content_type.value)

        if content_type.value == ContentType.music.value:
            name = "User Songs"
            value = "\U0001f3a7"

        else:
            name = "User Videos"
            value = "\U0001f4fa"

    elif service and not user:
        result = await bot.db.fetchrow("SELECT user_id, url, service FROM CONTENT WHERE service = $1 and content_type = $2 ORDER BY RANDOM()", service, content_type.value)   

        if content_type.value == ContentType.music.value:        
            name = "Service Songs"
            value = f"\U0001f5a5"

        else:
            name = "Service Videos"
            value = "\U0001f5a5"


    elif service and user:
        user_id = user.id
        result = await bot.db.fetchrow("SELECT user_id, url, service FROM CONTENT WHERE service = $1 and user_id = $2 and content_type = $3 ORDER BY RANDOM()", service, user_id, content_type.value)

        if content_type.value == ContentType.music.value:
            name = "User and Service Songs"
            value = "\U0001f3a7 \U0001f5a5"

        else:
            name = "User and Service Videos"
            value = "\U0001f4fa \U0001f5a5"

    result = result or await bot.db.fetchrow("SELECT user_id, url, service FROM CONTENT where content_type = $1 ORDER BY RANDOM()", content_type.value)
    name = name or "Randomly Chosen"
    value = value or "\U0001f570"

    user = await bot.try_user(result.user_id) or None
    return DatabaseData(result.url, result.service, user, name, value)
