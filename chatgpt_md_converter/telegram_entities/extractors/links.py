"""Link entity extraction."""

import re
from typing import List, Tuple

from ..entity import EntityType, TelegramEntity

# Pattern for Markdown links: [text](url)
# Also handles image links: ![alt](url) - treated the same as regular links
_LINK_PATTERN = re.compile(r"!?\[((?:[^\[\]]|\[.*?\])*)\]\(([^)]+)\)")


def extract_link_entities(
    text: str,
    existing_entities: List[TelegramEntity] | None = None,
) -> Tuple[str, List[TelegramEntity], List[TelegramEntity]]:
    """
    Extract Markdown links and return plain text with TEXT_LINK entities.

    Handles both regular links [text](url) and image links ![alt](url).
    Image links are converted to text links showing the alt text.

    Args:
        text: Input text with Markdown links
        existing_entities: Optional list of entities to adjust offsets for

    Returns:
        Tuple of (text_with_links_replaced, link_entities, adjusted_existing_entities)
    """
    entities: List[TelegramEntity] = []
    result_parts: List[str] = []
    last_end = 0

    # Track adjustments: list of (position_in_original, chars_removed)
    adjustments: List[Tuple[int, int]] = []

    for match in _LINK_PATTERN.finditer(text):
        # Add text before this link
        result_parts.append(text[last_end : match.start()])

        # Calculate position in output
        current_offset = sum(len(p) for p in result_parts)

        # Extract link text and URL
        link_text = match.group(1)
        url = match.group(2)

        # Calculate how many chars are removed
        # Original: [text](url) or ![text](url)
        # New: text
        chars_removed = len(match.group(0)) - len(link_text)
        adjustments.append((match.start(), chars_removed))

        # Add the link text (without the markdown syntax)
        result_parts.append(link_text)

        # Create entity
        entities.append(
            TelegramEntity(
                type=EntityType.TEXT_LINK,
                offset=current_offset,
                length=len(link_text),
                url=url,
            )
        )

        last_end = match.end()

    # Add remaining text
    result_parts.append(text[last_end:])

    # Adjust existing entities
    adjusted_existing: List[TelegramEntity] = []
    if existing_entities:
        for e in existing_entities:
            new_offset = e.offset
            # Apply all adjustments that occur before this entity
            for adj_pos, chars_removed in adjustments:
                if adj_pos < e.offset:
                    new_offset -= chars_removed
            adjusted_existing.append(
                TelegramEntity(
                    type=e.type,
                    offset=new_offset,
                    length=e.length,
                    url=e.url,
                    language=e.language,
                )
            )

    return "".join(result_parts), entities, adjusted_existing
