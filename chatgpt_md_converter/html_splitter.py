import re
from html.parser import HTMLParser

MAX_LENGTH = 4096
MIN_LENGTH = 500


class HTMLTagTracker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.open_tags = []

    def handle_starttag(self, tag, attrs):
        # saving tags
        if tag in (
                  "b", "i", "u", "s", "code", "pre", "a", "span", "blockquote",
                  "strong", "em", "ins", "strike", "del", "tg-spoiler", "tg-emoji"
                  ):
            self.open_tags.append((tag, attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.open_tags) - 1, -1, -1):
            if self.open_tags[i][0] == tag:
                del self.open_tags[i]
                break

    def get_open_tags_html(self):
        parts = []
        for tag, attrs in self.open_tags:
            attr_str = ""
            if attrs:
                attr_str = " " + " ".join(f'{k}="{v}"' for k, v in attrs)
            parts.append(f"<{tag}{attr_str}>")
        return "".join(parts)

    def get_closing_tags_html(self):
        return "".join(f"</{tag}>" for tag, _ in reversed(self.open_tags))


def split_pre_block(pre_block: str, max_length) -> list[str]:
    """
    Splits long HTML-formatted text into chunks suitable for sending via Telegram, 
    preserving valid HTML tag nesting and handling <pre>/<code> blocks separately.

    Args:
        text (str): The input HTML-formatted string.
        trim_leading_newlines (bool): If True, removes leading newline characters (`\\n`)
            from each resulting chunk before sending. This is useful to avoid 
            unnecessary blank space at the beginning of messages in Telegram.

    Returns:
        list[str]: A list of HTML-formatted message chunks, each within Telegram's length limit.
    """

    # language-aware: <pre><code class="language-python">...</code></pre>
    match = re.match(r"<pre><code(.*?)>(.*)</code></pre>", pre_block, re.DOTALL)
    if match:
        attr, content = match.groups()
        lines = content.splitlines(keepends=True)
        chunks, buf = [], ""
        overhead = len(f"<pre><code{attr}></code></pre>")
        for line in lines:
            if len(buf) + len(line) + overhead > max_length:
                chunks.append(f"<pre><code{attr}>{buf}</code></pre>")
                buf = ""
            buf += line
        if buf:
            chunks.append(f"<pre><code{attr}>{buf}</code></pre>")
        return chunks
    else:
        # regular <pre>...</pre>
        inner = pre_block[5:-6]
        lines = inner.splitlines(keepends=True)
        chunks, buf = [], ""
        overhead = len('<pre></pre>')
        for line in lines:
            if len(buf) + len(line) + overhead > max_length:
                chunks.append(f"<pre>{buf}</pre>")
                buf = ""
            buf += line
        if buf:
            chunks.append(f"<pre>{buf}</pre>")
        return chunks


def _is_only_tags(block: str) -> bool:
    return bool(re.fullmatch(r'(?:\s*<[^>]+>\s*)+', block))


def _effective_length(content: str) -> int:
    tracker = HTMLTagTracker()
    tracker.feed(content)
    return len(tracker.get_open_tags_html()) + len(content) + len(tracker.get_closing_tags_html())


def split_html_for_telegram(text: str, trim_empty_leadming_lines: bool = False, max_length: int = MAX_LENGTH) -> list[str]:
    """Split long HTML-formatted text into Telegram-compatible chunks.

    Parameters
    ----------
    text: str
        Input HTML text.
    trim_empty_leadming_lines: bool, optional
        If True, removes `\n` sybmols from start of chunks.
    max_length: int, optional
        Maximum allowed length for a single chunk (must be >= ``MIN_LENGTH = 500``).

    Returns
    -------
    list[str]
        List of HTML chunks.
    """

    if max_length < MIN_LENGTH:
        raise ValueError("max_length should be at least %d" % MIN_LENGTH)

    pattern = re.compile(r"(<pre>.*?</pre>|<pre><code.*?</code></pre>)", re.DOTALL)
    parts = pattern.split(text)

    chunks: list[str] = []
    prefix = ""
    current = ""

    def finalize():
        nonlocal current, prefix
        tracker = HTMLTagTracker()
        tracker.feed(prefix + current)
        chunk = prefix + current + tracker.get_closing_tags_html()
        chunks.append(chunk)
        prefix = tracker.get_open_tags_html()
        current = ""

    def append_piece(piece: str):
        nonlocal current, prefix
        if _effective_length(prefix + current + piece) <= max_length:
            current += piece
            return
        if len(piece) > max_length:
            if _is_only_tags(piece):
                raise ValueError("block contains only html tags")
            for word in re.split(r"(\s+)", piece):
                if not word:
                    continue
                append_piece(word)
            return
        if current:
            finalize()
            append_piece(piece)
        else:
            # piece itself doesn't fit with prefix; split by words
            for word in re.split(r"(\s+)", piece):
                if not word:
                    continue
                append_piece(word)

    for part in parts:
        if not part:
            continue
        if part.startswith("<pre>") or part.startswith("<pre><code"):
            pre_chunks = split_pre_block(part, max_length=max_length)
            for pc in pre_chunks:
                append_piece(pc)
            continue
        blocks = re.split(r"(\n\s*\n|<br\s*/?>|\n)", part)
        for block in blocks:
            if block:
                append_piece(block)

    if current:
        finalize()

    merged: list[str] = []
    buf = ""
    for chunk in chunks:
        if len(buf) + len(chunk) <= max_length:
            buf += chunk
        else:
            if buf:
                merged.append(buf)
            buf = chunk.lstrip("\n") if trim_empty_leadming_lines and merged else chunk
    if buf:
        merged.append(buf.lstrip("\n") if trim_empty_leadming_lines and merged else buf)

    return merged