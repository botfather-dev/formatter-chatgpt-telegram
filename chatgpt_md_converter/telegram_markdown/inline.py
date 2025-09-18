"""Inline text helpers for Telegram Markdown conversion."""

import re

_inline_code_pattern = re.compile(r"`([^`]+)`")
_italic_pattern = re.compile(
    r"(?<![A-Za-z0-9])\*(?=[^\s])(.*?)(?<!\s)\*(?![A-Za-z0-9])",
    re.DOTALL,
)


def convert_html_chars(text: str) -> str:
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def split_by_tag(out_text: str, md_tag: str, html_tag: str) -> str:
    tag_pattern = re.compile(
        r"(?<!\w){}(.*?){}(?!\w)".format(re.escape(md_tag), re.escape(md_tag)),
        re.DOTALL,
    )
    if html_tag == 'span class="tg-spoiler"':
        return tag_pattern.sub(r'<span class="tg-spoiler">\1</span>', out_text)
    return tag_pattern.sub(r"<{}>\1</{}>".format(html_tag, html_tag), out_text)


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
    return _italic_pattern.sub(r"<i>\1</i>", text)
