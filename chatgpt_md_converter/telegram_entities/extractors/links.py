"""Link entity extraction."""

import re
from typing import List, Tuple

from ..entity import EntityType, TelegramEntity

# Pattern for Markdown links: [text](url)
# Also handles image links: ![alt](url) - treated the same as regular links
_LINK_PATTERN = re.compile(r"!?\[((?:[^\[\]]|\[.*?\])*)\]\(([^)]+)\)")


def extract_link_entities(text: str) -> Tuple[str, List[TelegramEntity]]:
    """
    Extract Markdown links and return plain text with TEXT_LINK entities.

    Handles both regular links [text](url) and image links ![alt](url).
    Image links are converted to text links showing the alt text.

    Args:
        text: Input text with Markdown links

    Returns:
        Tuple of (text_with_links_replaced, list_of_entities)
    """
    entities: List[TelegramEntity] = []
    result_parts: List[str] = []
    last_end = 0

    for match in _LINK_PATTERN.finditer(text):
        # Add text before this link
        result_parts.append(text[last_end : match.start()])

        # Calculate position in output
        current_offset = sum(len(p) for p in result_parts)

        # Extract link text and URL
        link_text = match.group(1)
        url = match.group(2)

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

    return "".join(result_parts), entities
