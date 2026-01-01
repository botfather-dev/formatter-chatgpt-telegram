"""Heading entity extraction (converted to bold)."""

import re
from typing import List, Tuple

from ..entity import EntityType, TelegramEntity

# Pattern for Markdown headings: # Heading, ## Heading, etc.
_HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def extract_heading_entities(text: str) -> Tuple[str, List[TelegramEntity]]:
    """
    Extract Markdown headings and convert them to bold entities.

    Telegram doesn't have native heading support, so headings are converted
    to bold text (matching the HTML converter behavior).

    Args:
        text: Input text with Markdown headings

    Returns:
        Tuple of (text_with_headings_converted, list_of_bold_entities)
    """
    entities: List[TelegramEntity] = []
    result_parts: List[str] = []
    last_end = 0

    for match in _HEADING_PATTERN.finditer(text):
        # Add text before this heading
        result_parts.append(text[last_end : match.start()])

        # Calculate position in output
        current_offset = sum(len(p) for p in result_parts)

        # Extract heading text (without the # markers)
        heading_text = match.group(2)

        # Add the heading text
        result_parts.append(heading_text)

        # Create bold entity for the heading
        entities.append(
            TelegramEntity(
                type=EntityType.BOLD,
                offset=current_offset,
                length=len(heading_text),
            )
        )

        last_end = match.end()

    # Add remaining text
    result_parts.append(text[last_end:])

    return "".join(result_parts), entities
