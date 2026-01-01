"""Blockquote entity extraction."""

import re
from typing import List, Tuple

from ..entity import EntityType, TelegramEntity

# Pattern for regular blockquotes: > text
_BLOCKQUOTE_LINE_PATTERN = re.compile(r"^>(?!\*\*)\s?(.*)$", re.MULTILINE)

# Pattern for expandable blockquotes: >** text or **> text
_EXPANDABLE_BLOCKQUOTE_PATTERN = re.compile(
    r"^(?:>\*\*|\*\*>)\s?(.*)$", re.MULTILINE
)


def extract_blockquote_entities(text: str) -> Tuple[str, List[TelegramEntity]]:
    """
    Extract blockquotes and return plain text with BLOCKQUOTE entities.

    Handles both regular (>) and expandable (>** or **>) blockquotes.
    Consecutive blockquote lines are combined into a single entity.

    Args:
        text: Input text with blockquote markers

    Returns:
        Tuple of (text_without_markers, list_of_entities)
    """
    entities: List[TelegramEntity] = []

    # First, handle expandable blockquotes
    result_parts: List[str] = []

    # Find all expandable blockquote lines and group consecutive ones
    lines = text.split("\n")
    i = 0
    current_offset = 0

    while i < len(lines):
        line = lines[i]

        # Check for expandable blockquote
        exp_match = _EXPANDABLE_BLOCKQUOTE_PATTERN.match(line)
        if exp_match:
            # Collect consecutive expandable blockquote lines
            quote_lines = []

            while i < len(lines):
                m = _EXPANDABLE_BLOCKQUOTE_PATTERN.match(lines[i])
                if m:
                    quote_lines.append(m.group(1))
                    i += 1
                else:
                    break

            quote_content = "\n".join(quote_lines)
            quote_offset = current_offset
            current_offset += len(quote_content) + (1 if i < len(lines) else 0)

            result_parts.append(quote_content)
            if i < len(lines):
                result_parts.append("\n")

            entities.append(
                TelegramEntity(
                    type=EntityType.EXPANDABLE_BLOCKQUOTE,
                    offset=quote_offset,
                    length=len(quote_content),
                )
            )
            continue

        # Check for regular blockquote
        reg_match = _BLOCKQUOTE_LINE_PATTERN.match(line)
        if reg_match:
            # Collect consecutive regular blockquote lines
            quote_lines = []
            start_offset = current_offset

            while i < len(lines):
                # Don't match expandable as regular
                if _EXPANDABLE_BLOCKQUOTE_PATTERN.match(lines[i]):
                    break
                m = _BLOCKQUOTE_LINE_PATTERN.match(lines[i])
                if m:
                    quote_lines.append(m.group(1))
                    i += 1
                else:
                    break

            quote_content = "\n".join(quote_lines)
            current_offset += len(quote_content) + (1 if i < len(lines) else 0)

            result_parts.append(quote_content)
            if i < len(lines):
                result_parts.append("\n")

            entities.append(
                TelegramEntity(
                    type=EntityType.BLOCKQUOTE,
                    offset=start_offset,
                    length=len(quote_content),
                )
            )
            continue

        # Regular line
        current_offset += len(line) + (1 if i < len(lines) - 1 else 0)
        result_parts.append(line)
        if i < len(lines) - 1:
            result_parts.append("\n")
        i += 1

    result_text = "".join(result_parts)

    return result_text, entities
