"""Inline formatting entity extraction (bold, italic, underline, etc.)."""

import re
from typing import List, Tuple

from ..entity import EntityType, TelegramEntity

# Patterns for different formatting types
# Order matters - longer markers first to avoid partial matches
_PATTERNS = [
    # Bold+Italic: ***text***
    (
        re.compile(r"(?<![\\\*])\*\*\*(?!\*)(?=\S)([\s\S]*?)(?<=\S)\*\*\*(?!\*)", re.DOTALL),
        [EntityType.BOLD, EntityType.ITALIC],
        3,
    ),
    # Underline+Italic: ___text___
    (
        re.compile(
            r"(?<![\\_])___(?!_)(?=\S)([\s\S]*?)(?<=\S)___(?!_)",
            re.DOTALL,
        ),
        [EntityType.UNDERLINE, EntityType.ITALIC],
        3,
    ),
    # Bold: **text**
    (
        re.compile(r"(?<![\\\*])\*\*(?!\*)(?=\S)([\s\S]*?)(?<=\S)(?<!\*)\*\*(?!\*)", re.DOTALL),
        [EntityType.BOLD],
        2,
    ),
    # Underline: __text__
    (
        re.compile(
            r"(?<![\\_])__(?!_)(?=\S)([\s\S]*?)(?<=\S)(?<!_)__(?!_)",
            re.DOTALL,
        ),
        [EntityType.UNDERLINE],
        2,
    ),
    # Strikethrough: ~~text~~
    (
        re.compile(r"(?<![\\~])~~(?!~)(?=\S)([\s\S]*?)(?<=\S)(?<!~)~~(?!~)", re.DOTALL),
        [EntityType.STRIKETHROUGH],
        2,
    ),
    # Spoiler: ||text||
    (
        re.compile(r"(?<![\\|])\|\|(?!\|)(?=\S)([^\n]*?)(?<=\S)(?<!\|)\|\|(?!\|)"),
        [EntityType.SPOILER],
        2,
    ),
    # Italic with asterisk: *text* (must not be adjacent to other asterisks)
    (
        re.compile(
            r"(?<![A-Za-z0-9\\\*])\*(?!\*)(?=\S)([\s\S]*?)(?<=\S)(?<!\*)\*(?![A-Za-z0-9\*])",
            re.DOTALL,
        ),
        [EntityType.ITALIC],
        1,
    ),
    # Italic with underscore: _text_
    (
        re.compile(
            r"(?<![A-Za-z0-9\\_])_(?!_)(?=\S)([\s\S]*?)(?<=\S)(?<!_)_(?![A-Za-z0-9_])",
            re.DOTALL,
        ),
        [EntityType.ITALIC],
        1,
    ),
]


class _Match:
    """Represents a formatting match with its properties."""

    def __init__(
        self,
        start: int,
        end: int,
        inner_start: int,
        inner_end: int,
        entity_types: List[EntityType],
        marker_len: int,
    ):
        self.start = start
        self.end = end
        self.inner_start = inner_start
        self.inner_end = inner_end
        self.entity_types = entity_types
        self.marker_len = marker_len
        self.children: List["_Match"] = []

    def contains(self, other: "_Match") -> bool:
        """Check if this match's inner content fully contains another match."""
        return self.inner_start <= other.start and other.end <= self.inner_end


def _find_all_matches(text: str) -> List[_Match]:
    """Find all formatting matches in text."""
    matches = []

    for pattern, entity_types, marker_len in _PATTERNS:
        for match in pattern.finditer(text):
            matches.append(
                _Match(
                    start=match.start(),
                    end=match.end(),
                    inner_start=match.start() + marker_len,
                    inner_end=match.end() - marker_len,
                    entity_types=list(entity_types),
                    marker_len=marker_len,
                )
            )

    # Sort by start position, then by length descending (longer first)
    matches.sort(key=lambda m: (m.start, -(m.end - m.start)))

    return matches


def _build_match_tree(matches: List[_Match]) -> List[_Match]:
    """
    Build a tree of matches where nested matches are children.
    Returns only top-level matches (others are nested as children).
    """
    if not matches:
        return []

    result: List[_Match] = []

    for match in matches:
        # Find if this match should be nested inside an existing result
        placed = False
        for existing in result:
            if existing.contains(match):
                # Recursively try to place in existing's children
                placed = _try_place_in_children(existing, match)
                if placed:
                    break

        if not placed:
            # Check if this match overlaps with any existing (invalid)
            overlaps = False
            for existing in result:
                if _matches_overlap(match, existing):
                    overlaps = True
                    break

            if not overlaps:
                result.append(match)

    return result


def _try_place_in_children(parent: _Match, child: _Match) -> bool:
    """Try to place a child match in the parent's children list."""
    # First check if it fits in any existing child
    for existing_child in parent.children:
        if existing_child.contains(child):
            return _try_place_in_children(existing_child, child)

    # Check for overlaps with existing children
    for existing_child in parent.children:
        if _matches_overlap(child, existing_child):
            return False

    # Can add as a direct child
    parent.children.append(child)
    return True


def _matches_overlap(m1: _Match, m2: _Match) -> bool:
    """Check if two matches have invalid overlap (partial, not nested)."""
    # No overlap
    if m1.end <= m2.start or m2.end <= m1.start:
        return False
    # m1 contains m2 in inner content
    if m1.inner_start <= m2.start and m2.end <= m1.inner_end:
        return False
    # m2 contains m1 in inner content
    if m2.inner_start <= m1.start and m1.end <= m2.inner_end:
        return False
    # Invalid overlap
    return True


def _process_match(
    text: str,
    match: _Match,
    base_offset: int,
) -> Tuple[str, List[TelegramEntity]]:
    """
    Process a single match and its children, returning plain text and entities.

    Args:
        text: The text containing the match
        match: The match to process
        base_offset: Offset in the final output where this match starts

    Returns:
        Tuple of (processed_text, entities)
    """
    inner_text = text[match.inner_start : match.inner_end]
    entities: List[TelegramEntity] = []

    # If there are children, process them
    if match.children:
        # Sort children by position
        match.children.sort(key=lambda m: m.start)

        # Process children recursively
        processed_parts: List[str] = []
        child_entities: List[TelegramEntity] = []
        last_end = match.inner_start

        for child in match.children:
            # Add text before this child
            processed_parts.append(text[last_end : child.start])

            # Calculate child's offset in the final output
            child_offset = base_offset + sum(len(p) for p in processed_parts)

            # Process child recursively
            child_text, child_ents = _process_match(text, child, child_offset)
            processed_parts.append(child_text)
            child_entities.extend(child_ents)

            last_end = child.end

        # Add remaining text after last child
        processed_parts.append(text[last_end : match.inner_end])

        inner_text = "".join(processed_parts)
        entities.extend(child_entities)

    # Create entities for this match
    for entity_type in match.entity_types:
        entities.append(
            TelegramEntity(
                type=entity_type,
                offset=base_offset,
                length=len(inner_text),
            )
        )

    return inner_text, entities


def extract_inline_formatting_entities(
    text: str,
) -> Tuple[str, List[TelegramEntity]]:
    """
    Extract inline formatting (bold, italic, etc.) and return plain text with entities.

    Handles nested formatting where one style is fully contained within another.

    Args:
        text: Input text with Markdown formatting markers

    Returns:
        Tuple of (text_without_markers, list_of_entities)
    """
    matches = _find_all_matches(text)
    top_level_matches = _build_match_tree(matches)

    if not top_level_matches:
        return text, []

    # Sort by position
    top_level_matches.sort(key=lambda m: m.start)

    # Process all matches
    result_parts: List[str] = []
    all_entities: List[TelegramEntity] = []
    last_end = 0

    for match in top_level_matches:
        # Add text before this match
        result_parts.append(text[last_end : match.start])

        # Calculate offset for this match
        current_offset = sum(len(p) for p in result_parts)

        # Process match and its children
        processed_text, entities = _process_match(text, match, current_offset)
        result_parts.append(processed_text)
        all_entities.extend(entities)

        last_end = match.end

    # Add remaining text
    result_parts.append(text[last_end:])

    return "".join(result_parts), all_entities
