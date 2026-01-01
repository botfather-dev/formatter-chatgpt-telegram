"""
Telegram entity conversion module.

This module provides functions to convert Markdown text to Telegram's
native entity format (plain text + MessageEntity objects).
"""

from typing import List, Tuple

from .entity import EntityType, TelegramEntity
from .parser import parse_entities


def telegram_format_entities(text: str) -> Tuple[str, List[dict]]:
    """
    Convert Markdown text to Telegram format with entities.

    This function parses Markdown syntax and returns plain text along with
    a list of entity dictionaries suitable for the Telegram Bot API.

    Supported Markdown elements:
    - **bold**
    - *italic* or _italic_
    - __underline__
    - ~~strikethrough~~
    - ||spoiler||
    - `inline code`
    - ```language
      code blocks
      ```
    - [link text](url)
    - > blockquotes
    - >** expandable blockquotes
    - # Headings (converted to bold)
    - Lists with - or *

    Args:
        text: Markdown-formatted text

    Returns:
        Tuple of (plain_text, entities) where:
        - plain_text: Text with all Markdown markers removed
        - entities: List of dicts with 'type', 'offset', 'length' keys
          (plus 'url' for links, 'language' for code blocks)

    Example:
        >>> text, entities = telegram_format_entities("**Hello** world!")
        >>> print(text)
        Hello world!
        >>> print(entities)
        [{'type': 'bold', 'offset': 0, 'length': 5}]

        # Use with python-telegram-bot:
        await bot.send_message(chat_id, text=text, entities=entities)

        # Use with aiogram:
        await message.answer(text, entities=entities)
    """
    plain_text, entity_objects = parse_entities(text)
    return plain_text, [e.to_dict() for e in entity_objects]


__all__ = [
    "telegram_format_entities",
    "TelegramEntity",
    "EntityType",
    "parse_entities",
]
