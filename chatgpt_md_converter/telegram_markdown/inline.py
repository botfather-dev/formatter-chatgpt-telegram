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

_VOID_TAGS = {"br", "hr", "img", "input", "link", "meta"}


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

        if not inner.strip():
            return match.group(0)

        if md_tag == "**" and not re.search(r"[^\s*]", inner):
            return match.group(0)

        if html_tag == 'span class="tg-spoiler"':
            return f'<span class="tg-spoiler">{inner}</span>'
        return f"<{html_tag}>{inner}</{html_tag}>"

    return pattern.sub(_wrap, out_text)


def extract_inline_code_snippets(text: str):
    placeholders: list[str] = []
    snippets: dict[str, str] = {}

    def replacer(match: re.Match[str]) -> str:
        snippet = match.group(1)
        placeholder = f"INLINECODEPLACEHOLDER_{len(placeholders)}_"
        placeholders.append(placeholder)
        snippets[placeholder] = snippet
        return placeholder

    modified = _inline_code_pattern.sub(replacer, text)
    return modified, snippets


def _tag_stack_at_stars(text: str) -> dict[int, tuple[str, ...]]:
    star_positions = {match.start() for match in re.finditer(r"\*", text)}
    stack: list[str] = []
    stack_at: dict[int, tuple[str, ...]] = {}

    i = 0
    text_len = len(text)
    while i < text_len:
        if i in star_positions:
            stack_at[i] = tuple(stack)
        if text[i] == "<":
            tag_end = text.find(">", i + 1)
            if tag_end == -1:
                i += 1
                continue
            tag_content = text[i + 1 : tag_end].strip()
            if tag_content:
                is_closing = tag_content.startswith("/")
                if is_closing:
                    tag_name = tag_content[1:].split()[0].lower()
                    if stack and stack[-1] == tag_name:
                        stack.pop()
                else:
                    tag_name = tag_content.split()[0].lower().rstrip("/")
                    is_self_closing = tag_content.endswith("/") or tag_name in _VOID_TAGS
                    if not is_self_closing:
                        stack.append(tag_name)
            i = tag_end + 1
            continue
        i += 1

    return stack_at


def apply_custom_italic(text: str) -> str:
    stack_at = _tag_stack_at_stars(text)

    def _wrap(match: re.Match[str]) -> str:
        start = match.start()
        end = match.end() - 1
        start_stack = stack_at.get(start)
        end_stack = stack_at.get(end)
        if start_stack is None or end_stack is None or start_stack != end_stack:
            return match.group(0)
        return f"<i>{match.group(1)}</i>"

    return _ITALIC_STAR_PATTERN.sub(_wrap, text)
