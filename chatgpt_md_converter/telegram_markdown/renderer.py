"""High-level Telegram Markdown → HTML renderer."""

from __future__ import annotations

import re

from .code_blocks import extract_and_convert_code_blocks, reinsert_code_blocks
from .html_escape import escape_code_content
from .inline import (apply_custom_italic, convert_html_chars,
                     extract_inline_code_snippets, split_by_tag)
from .postprocess import remove_blockquote_escaping, remove_spoiler_escaping
from .preprocess import combine_blockquotes


def telegram_format(text: str) -> str:
    output, block_map = extract_and_convert_code_blocks(text)
    output = combine_blockquotes(output)
    output, inline_snippets = extract_inline_code_snippets(output)

    output = convert_html_chars(output)

    output = re.sub(r"^(#{1,6})\s+(.+)$", r"<b>\2</b>", output, flags=re.MULTILINE)
    output = re.sub(r"^(\s*)[\-\*]\s+(.+)$", r"\1• \2", output, flags=re.MULTILINE)

    def _replace_triple_star(match: re.Match[str]) -> str:
        inner = match.group(1)
        if not inner.strip():
            return match.group(0)
        return f"<b><i>{inner}</i></b>"

    def _replace_triple_underscore(match: re.Match[str]) -> str:
        inner = match.group(1)
        if not inner.strip():
            return match.group(0)
        return f"<u><i>{inner}</i></u>"

    output = re.sub(
        r"(?<!\*)\*\*\*(?!\*)(.*?)(?<!\*)\*\*\*(?!\*)",
        _replace_triple_star,
        output,
        flags=re.DOTALL,
    )
    output = re.sub(
        r"(?<!_)___(?!_)(.*?)(?<!_)___(?!_)",
        _replace_triple_underscore,
        output,
        flags=re.DOTALL,
    )

    output = split_by_tag(output, "**", "b")
    output = split_by_tag(output, "__", "u")
    output = split_by_tag(output, "~~", "s")
    output = split_by_tag(output, "||", 'span class="tg-spoiler"')

    output = apply_custom_italic(output)
    output = split_by_tag(output, "_", "i")

    output = re.sub(r"【[^】]+】", "", output)

    # Handle Telegram custom emoji before generic links
    # ![emoji](tg://emoji?id=123) -> <tg-emoji emoji-id="123">emoji</tg-emoji>
    emoji_pattern = r"!\[([^\]]*)\]\(tg://emoji\?id=(\d+)\)"
    output = re.sub(emoji_pattern, r'<tg-emoji emoji-id="\2">\1</tg-emoji>', output)

    # Handle all links including images (! prefix is stripped for non-emoji images)
    link_pattern = r"(?:!?)\[((?:[^\[\]]|\[.*?\])*)\]\(([^)]+)\)"
    output = re.sub(link_pattern, r'<a href="\2">\1</a>', output)

    for placeholder, snippet in inline_snippets.items():
        escaped = escape_code_content(snippet)
        output = output.replace(placeholder, f"<code>{escaped}</code>")

    output = reinsert_code_blocks(output, block_map)
    output = remove_blockquote_escaping(output)
    output = remove_spoiler_escaping(output)

    output = re.sub(r"\n{3,}", "\n\n", output)

    return output.strip()
