"""Telegram entity data structures."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EntityType(Enum):
    """Telegram MessageEntity types."""

    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    STRIKETHROUGH = "strikethrough"
    SPOILER = "spoiler"
    CODE = "code"
    PRE = "pre"
    TEXT_LINK = "text_link"
    BLOCKQUOTE = "blockquote"
    EXPANDABLE_BLOCKQUOTE = "expandable_blockquote"


@dataclass
class TelegramEntity:
    """
    Represents a Telegram MessageEntity.

    Attributes:
        type: The entity type (bold, italic, code, etc.)
        offset: Start position in UTF-16 code units
        length: Length in UTF-16 code units
        url: URL for TEXT_LINK entities
        language: Programming language for PRE (code block) entities
    """

    type: EntityType
    offset: int
    length: int
    url: Optional[str] = None
    language: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dict for JSON serialization / Telegram API."""
        result = {
            "type": self.type.value,
            "offset": self.offset,
            "length": self.length,
        }
        if self.url is not None:
            result["url"] = self.url
        if self.language is not None:
            result["language"] = self.language
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "TelegramEntity":
        """Create entity from dictionary."""
        return cls(
            type=EntityType(data["type"]),
            offset=data["offset"],
            length=data["length"],
            url=data.get("url"),
            language=data.get("language"),
        )
