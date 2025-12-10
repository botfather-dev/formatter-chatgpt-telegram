"""High-level Telegram Markdown → HTML renderer."""

from __future__ import annotations

import re

from .code_blocks import extract_and_convert_code_blocks, reinsert_code_blocks
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

    output = re.sub(r"\*\*\*(.*?)\*\*\*", r"<b><i>\1</i></b>", output)
    output = re.sub(r"\_\_\_(.*?)\_\_\_", r"<u><i>\1</i></u>", output)

    output = split_by_tag(output, "**", "b")
    output = split_by_tag(output, "__", "u")
    output = split_by_tag(output, "~~", "s")
    output = split_by_tag(output, "||", 'span class="tg-spoiler"')

    output = apply_custom_italic(output)
    output = split_by_tag(output, "_", "i")

    output = re.sub(r"【[^】]+】", "", output)

    link_pattern = r"(?:!?)\[((?:[^\[\]]|\[.*?\])*)\]\(([^)]+)\)"
    output = re.sub(link_pattern, r'<a href="\2">\1</a>', output)

    for placeholder, snippet in inline_snippets.items():
        escaped = (
            snippet.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        output = output.replace(placeholder, f"<code>{escaped}</code>")

    output = reinsert_code_blocks(output, block_map)
    output = remove_blockquote_escaping(output)
    output = remove_spoiler_escaping(output)

    output = re.sub(r"\n{3,}", "\n\n", output)

    return output.strip()
