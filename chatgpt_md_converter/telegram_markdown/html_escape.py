"""HTML escaping utilities for code content.

LLMs sometimes pre-escape HTML entities (&lt; &gt; &amp; &quot;) in
markdown code blocks and inline code. We unescape first, then
re-escape exactly once to avoid double-escaping like &amp;lt;.
"""

import re

_HTML_ENTITY_RE = re.compile(r"&(?:lt|gt|amp|quot|apos|#\d+|#x[\da-fA-F]+);")


def _is_pre_escaped(text: str) -> bool:
    """Return True if the text contains any HTML character references."""
    return bool(_HTML_ENTITY_RE.search(text))


def _unescape_html(text: str) -> str:
    """Unescape common HTML character references to their literal chars."""
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", '"')
    text = text.replace("&apos;", "'")
    return text


def escape_code_content(text: str) -> str:
    """Escape code content for Telegram HTML, handling pre-escaped input.

    If the input already contains HTML entities (from LLM pre-escaping),
    unescape them first so we produce a single level of escaping.
    """
    if _is_pre_escaped(text):
        text = _unescape_html(text)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
