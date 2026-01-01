"""Main parser that combines all entity extractors."""

import re
from typing import List, Tuple

from .entity import EntityType, TelegramEntity
from .extractors import (extract_blockquote_entities, extract_heading_entities,
                         extract_inline_formatting_entities,
                         extract_link_entities)
from .utf16 import utf16_len

# Placeholder prefix for protected content
_CODE_BLOCK_PLACEHOLDER = "\x00CODEBLOCK"
_INLINE_CODE_PLACEHOLDER = "\x00INLINECODE"


def _convert_list_markers(text: str) -> str:
    """Convert Markdown list markers (* or -) to bullet points."""
    return re.sub(r"^(\s*)[\-\*]\s+", r"\1• ", text, flags=re.MULTILINE)


def _remove_citation_markers(text: str) -> str:
    """Remove ChatGPT-style citation markers like 【1】."""
    return re.sub(r"【[^】]+】", "", text)


def _adjust_entities_to_utf16(
    text: str, entities: List[TelegramEntity]
) -> List[TelegramEntity]:
    """
    Convert entity offsets and lengths from Python char indices to UTF-16 code units.

    Telegram requires UTF-16 code units for entity positions.
    """
    adjusted = []
    for entity in entities:
        # Clamp offset and length to text bounds
        offset = min(entity.offset, len(text))
        length = min(entity.length, len(text) - offset)

        if length <= 0:
            continue

        # Get the text portions
        before_text = text[:offset]
        entity_text = text[offset : offset + length]

        # Convert to UTF-16 units
        utf16_offset = utf16_len(before_text)
        utf16_length = utf16_len(entity_text)

        if utf16_length > 0:
            adjusted.append(
                TelegramEntity(
                    type=entity.type,
                    offset=utf16_offset,
                    length=utf16_length,
                    url=entity.url,
                    language=entity.language,
                )
            )

    return adjusted


def _validate_and_sort_entities(
    entities: List[TelegramEntity],
) -> List[TelegramEntity]:
    """
    Sort entities by offset and filter invalid ones.
    """
    # Filter out zero-length and negative entities
    entities = [e for e in entities if e.length > 0 and e.offset >= 0]

    # Sort by offset, then by length descending (longer first for nesting)
    entities = sorted(entities, key=lambda e: (e.offset, -e.length))

    return entities


def _clean_multiple_newlines(text: str) -> str:
    """Reduce 3+ consecutive newlines to just 2."""
    return re.sub(r"\n{3,}", "\n\n", text)


def _extract_with_placeholders(
    text: str, pattern: re.Pattern, placeholder_prefix: str
) -> Tuple[str, dict]:
    """
    Extract matches and replace with placeholders.
    Returns (modified_text, {placeholder: (content, entity_info)})
    """
    extractions = {}
    counter = [0]

    def replacer(match):
        placeholder = f"{placeholder_prefix}{counter[0]}\x00"
        counter[0] += 1
        extractions[placeholder] = match
        return placeholder

    modified = pattern.sub(replacer, text)
    return modified, extractions


def parse_entities(text: str) -> Tuple[str, List[TelegramEntity]]:
    """
    Parse Markdown text and return plain text with Telegram entities.

    Uses a placeholder-based approach to handle the order of extraction correctly:
    1. Replace code blocks and inline code with placeholders
    2. Extract all other formatting (blockquotes, headings, links, inline styles)
    3. Restore placeholders and calculate final offsets

    Args:
        text: Markdown-formatted text

    Returns:
        Tuple of (plain_text, list_of_entities)
        Entities have offsets/lengths in UTF-16 code units.
    """
    all_entities: List[TelegramEntity] = []

    # Phase 1: Extract code blocks to placeholders
    code_block_pattern = re.compile(
        r"(?P<fence>`{3,})(?P<lang>\w+)?\n(?P<code>[\s\S]*?)(?P=fence)",
        flags=re.MULTILINE,
    )
    code_block_map = {}
    code_block_counter = [0]

    def replace_code_block(match):
        placeholder = f"{_CODE_BLOCK_PLACEHOLDER}{code_block_counter[0]}\x00"
        code_block_counter[0] += 1
        # Strip trailing newline from code content (appears before closing fence)
        code_content = match.group("code").rstrip("\n")
        language = match.group("lang") or None
        code_block_map[placeholder] = (code_content, language)
        return placeholder

    # Ensure closing delimiters
    text = _ensure_closing_delimiters(text)
    text = code_block_pattern.sub(replace_code_block, text)

    # Phase 2: Extract inline code to placeholders
    inline_code_pattern = re.compile(r"`([^`\n]+)`")
    inline_code_map = {}
    inline_code_counter = [0]

    def replace_inline_code(match):
        placeholder = f"{_INLINE_CODE_PLACEHOLDER}{inline_code_counter[0]}\x00"
        inline_code_counter[0] += 1
        code_content = match.group(1)
        inline_code_map[placeholder] = code_content
        return placeholder

    text = inline_code_pattern.sub(replace_inline_code, text)

    # Phase 3: Extract other formatting (on text with placeholders)
    # Order matters: inline formatting first (removes markers), then links
    text, blockquote_entities = extract_blockquote_entities(text)
    all_entities.extend(blockquote_entities)

    text, heading_entities = extract_heading_entities(text)
    all_entities.extend(heading_entities)

    text, inline_entities = extract_inline_formatting_entities(text)
    all_entities.extend(inline_entities)

    # Extract links AFTER inline formatting, adjusting existing entity offsets
    text, link_entities, all_entities = extract_link_entities(text, all_entities)
    all_entities.extend(link_entities)

    # Phase 4: Restore code placeholders and create entities
    # Collect all placeholders with their info
    all_placeholders = []

    for placeholder, (code_content, language) in code_block_map.items():
        if placeholder in text:
            pos = text.find(placeholder)
            all_placeholders.append({
                'placeholder': placeholder,
                'content': code_content,
                'position': pos,
                'type': EntityType.PRE,
                'language': language,
            })

    for placeholder, code_content in inline_code_map.items():
        if placeholder in text:
            pos = text.find(placeholder)
            all_placeholders.append({
                'placeholder': placeholder,
                'content': code_content,
                'position': pos,
                'type': EntityType.CODE,
                'language': None,
            })

    # Sort by position ascending (restore from start to end)
    # This way, when we shift entities, the later entities get adjusted correctly
    all_placeholders.sort(key=lambda x: x['position'])

    code_entities: List[TelegramEntity] = []

    for ph_info in all_placeholders:
        placeholder = ph_info['placeholder']
        code_content = ph_info['content']
        offset = text.find(placeholder)
        text = text.replace(placeholder, code_content, 1)

        code_entities.append(
            TelegramEntity(
                type=ph_info['type'],
                offset=offset,
                length=len(code_content),
                language=ph_info['language'],
            )
        )

        # Adjust existing entities (both all_entities and code_entities) after this position
        placeholder_len = len(placeholder)
        content_len = len(code_content)
        shift = content_len - placeholder_len
        all_entities = _shift_entities_after(all_entities, offset, shift)
        # Also shift already-created code entities (except the one we just added)
        code_entities = _shift_entities_after(code_entities[:-1], offset, shift) + [code_entities[-1]]

    all_entities.extend(code_entities)

    # Phase 5: Clean up
    text = _convert_list_markers(text)
    text = _remove_citation_markers(text)
    text = _clean_multiple_newlines(text)

    # Validate and sort entities
    all_entities = _validate_and_sort_entities(all_entities)

    # Convert to UTF-16 offsets
    all_entities = _adjust_entities_to_utf16(text, all_entities)

    return text.strip(), all_entities


def _shift_entities_after(
    entities: List[TelegramEntity], position: int, shift: int
) -> List[TelegramEntity]:
    """Shift entity offsets that come after a given position."""
    result = []
    for e in entities:
        if e.offset >= position:
            result.append(
                TelegramEntity(
                    type=e.type,
                    offset=e.offset + shift,
                    length=e.length,
                    url=e.url,
                    language=e.language,
                )
            )
        else:
            result.append(e)
    return result


def _ensure_closing_delimiters(text: str) -> str:
    """Append any missing closing backtick fences for Markdown code blocks."""
    code_block_re = re.compile(
        r"(?P<fence>`{3,})(?P<lang>\w+)?\n?[\s\S]*?(?<=\n)?(?P=fence)",
        flags=re.DOTALL,
    )

    open_fence = None
    for line in text.splitlines():
        stripped = line.strip()
        if open_fence is None:
            match = re.match(r"^(?P<fence>`{3,})(?P<lang>\w+)?$", stripped)
            if match:
                open_fence = match.group("fence")
        else:
            if stripped == open_fence:
                open_fence = None

    if open_fence is not None:
        if not text.endswith("\n"):
            text += "\n"
        text += open_fence

    # Check for unclosed triple backticks
    temp = code_block_re.sub("", text)
    if temp.count("```") % 2 != 0:
        text += "\n```"

    # Check for unclosed single backticks (inline code)
    temp = code_block_re.sub("", text)
    temp = re.sub(r"``+", "", temp)
    if temp.count("`") % 2 != 0:
        text += "`"

    return text
