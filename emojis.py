import discord

import json
from random import choice

DEFAULT_EMOJI_UNICODE = "U+1F633" # Flushed Face

EMOJIS_FILE = "config/emoji_catalogue.json"

with open(EMOJIS_FILE, "r") as f:
    _emojis = json.load(f)

# assert all emojis have different name and id
assert len(_emojis) == len({e["name"] for e in _emojis}), "Emoji names must be unique"
assert len(_emojis) == len({e["id"] for e in _emojis}), "Emoji IDs must be unique"

def get_app_emoji(name: str) -> str:
    """Get an emoji listed on the developer portal
    Args:
        name (str): The name of the emoji as listed on the developer portal
    """
    assert isinstance(name, str), "Emoji name must be a string"
    assert len(name) > 0, "Emoji name cannot be empty"
    
    emoji_data = next(filter(lambda e: e["name"] == name, _emojis))
    if not emoji_data:
        raise ValueError(f"Emoji '{name}' not found in emoji catalogue")
    
    emoji_str = "<" + ':'.join([
        'a' if emoji_data["animated"] else '',
        emoji_data["name"],
        str(emoji_data["id"])
    ]) + ">"
    return emoji_str
    

def get_server_emoji(ctx: discord.ApplicationContext, name: str = None) -> str:
    """Get a server emoji by name. If no name is given, return a random emoji.
    Args:
        guild (discord.Guild): The guild to get the emoji from
        name (str): The name of the emoji
    """
    assert isinstance(ctx, discord.ApplicationContext), "ctx must be an ApplicationContext"

    guild_emojis = ctx.guild.emojis
    if not guild_emojis:
        return __get_emoji_from_unicode(DEFAULT_EMOJI_UNICODE)
    emoji: discord.Emoji
    if name:
        assert isinstance(name, str), "Emoji name must be a string"
        assert len(name) > 0, "Emoji name cannot be empty"
        emoji = next(filter(lambda e: e.name == name, guild_emojis))
        if not emoji:
            raise ValueError(f"Emoji '{name}' not found in guild '{ctx.guild.name}'")
    else:
        emoji = choice(guild_emojis)

    emoji_str = "<" + ":".join([
        'a' if emoji.animated else '',
        emoji.name,
        str(emoji.id)
    ]) + ">"
    return emoji_str

def __get_emoji_from_unicode(unicode: str) -> str:
    """Get an emoji from its unicode representation
    Args:
        unicode (str): The unicode representation of the emoji
    """
    assert isinstance(unicode, str), "Unicode must be a string"
    assert unicode.startswith("U+"), "Unicode must start with 'U+'"
    
    try:
        emoji_str = chr(int(unicode.replace("U+", ""), 16))
    except ValueError:
        raise ValueError(f"Invalid unicode: {unicode}")
    
    return emoji_str