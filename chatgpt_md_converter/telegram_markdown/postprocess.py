"""Post-processing helpers for Telegram Markdown conversion."""


def remove_blockquote_escaping(output: str) -> str:
    """Unescape blockquote tags produced during formatting."""
    output = output.replace("&lt;blockquote&gt;", "<blockquote>").replace(
        "&lt;/blockquote&gt;", "</blockquote>"
    )
    output = output.replace(
        "&lt;blockquote expandable&gt;", "<blockquote expandable>"
    ).replace("&lt;/blockquote&gt;", "</blockquote>")
    return output


def remove_spoiler_escaping(output: str) -> str:
    """Ensure spoiler spans remain HTML tags, not escaped text."""
    output = output.replace(
        '&lt;span class="tg-spoiler"&gt;', '<span class="tg-spoiler">'
    )
    output = output.replace("&lt;/span&gt;", "</span>")
    return output
