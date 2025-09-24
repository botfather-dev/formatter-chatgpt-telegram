"""Inline text helpers for Telegram Markdown conversion."""

import re

_inline_code_pattern = re.compile(r"`([^`]+)`")

_BOLD_PATTERN = re.compile(r"(?<!\\)\*\*(?=\S)(.*?)(?<=\S)\*\*", re.DOTALL)
_UNDERLINE_PATTERN = re.compile(
    r"(?<!\\)(?<![A-Za-z0-9_])__(?=\S)(.*?)(?<=\S)__(?![A-Za-z0-9_])",
    re.DOTALL,
)
_ITALIC_UNDERSCORE_PATTERN = re.compile(
    r"(?<!\\)(?<![A-Za-z0-9_])_(?=\S)(.*?)(?<=\S)_(?![A-Za-z0-9_])",
    re.DOTALL,
)
_STRIKETHROUGH_PATTERN = re.compile(r"(?<!\\)~~(?=\S)(.*?)(?<=\S)~~", re.DOTALL)
_SPOILER_PATTERN = re.compile(r"(?<!\\)\|\|(?=\S)([^\n]*?)(?<=\S)\|\|")
_ITALIC_STAR_PATTERN = re.compile(
    r"(?<![A-Za-z0-9\\])\*(?!\*)(?=[^\s])(.*?)(?<![\s\\])\*(?![A-Za-z0-9\\])",
    re.DOTALL,
)

_PATTERN_MAP = {
    "**": _BOLD_PATTERN,
    "__": _UNDERLINE_PATTERN,
    "_": _ITALIC_UNDERSCORE_PATTERN,
    "~~": _STRIKETHROUGH_PATTERN,
    "||": _SPOILER_PATTERN,
}


def convert_html_chars(text: str) -> str:
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def split_by_tag(out_text: str, md_tag: str, html_tag: str) -> str:
    pattern = _PATTERN_MAP.get(md_tag)
    if pattern is None:
        escaped = re.escape(md_tag)
        pattern = re.compile(
            rf"(?<!\\){escaped}(?=\S)(.*?)(?<=\S){escaped}",
            re.DOTALL,
        )

    def _wrap(match: re.Match[str]) -> str:
        inner = match.group(1)
        if html_tag == 'span class="tg-spoiler"':
            return f'<span class="tg-spoiler">{inner}</span>'
        return f"<{html_tag}>{inner}</{html_tag}>"

    return pattern.sub(_wrap, out_text)


def extract_inline_code_snippets(text: str):
    placeholders: list[str] = []
    snippets: dict[str, str] = {}

    def replacer(match: re.Match[str]) -> str:
        snippet = match.group(1)
        placeholder = f"INLINECODEPLACEHOLDER{len(placeholders)}"
        placeholders.append(placeholder)
        snippets[placeholder] = snippet
        return placeholder

    modified = _inline_code_pattern.sub(replacer, text)
    return modified, snippets


def apply_custom_italic(text: str) -> str:
    return _ITALIC_STAR_PATTERN.sub(r"<i>\1</i>", text)
