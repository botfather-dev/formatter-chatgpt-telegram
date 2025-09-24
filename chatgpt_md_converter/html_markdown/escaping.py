"""Shared escaping utilities for Telegram Markdown conversion."""

from __future__ import annotations

import html
import re

from .tree import Node

_SIMPLE_STAR_ITALIC = re.compile(
    r"(?<!\\)(?<!\*)\*(?=[^\s])([^\*\n]+?)(?<!\s)\*(?![A-Za-z0-9\*])",
)


def _canonicalize_star_italics(text: str) -> str:
    def _replace(match: re.Match[str]) -> str:
        inner = match.group(1)
        if "*" in inner or "_" in inner or "`" in inner:
            return match.group(0)
        return f"_{inner}_"

    return _SIMPLE_STAR_ITALIC.sub(_replace, text)


def normalise_text(text: str) -> str:
    if not text:
        return ""
    unescaped = html.unescape(text)
    return unescaped.replace("\u00a0", " ")


def collect_text(node: Node) -> str:
    if node.kind == "text":
        return html.unescape(node.text)
    parts: list[str] = []
    for child in node.children:
        if child.kind == "text":
            parts.append(html.unescape(child.text))
        elif child.kind == "element":
            if child.tag.lower() == "br":
                parts.append("\n")
            else:
                parts.append(collect_text(child))
    return "".join(parts)


def escape_inline_code(text: str) -> str:
    return text.replace("`", "\\`")


def escape_link_label(label: str) -> str:
    escaped = label
    for ch in "[]()":
        escaped = escaped.replace(ch, f"\\{ch}")
    return escaped


def escape_link_url(url: str) -> str:
    return url.replace("\\", "\\\\").replace(")", "\\)")


def post_process(markdown: str) -> str:
    text = re.sub(r"(^|\n)•\s", r"\1- ", markdown)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.replace("\r", "")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = _canonicalize_star_italics(text)
    return text.strip()
