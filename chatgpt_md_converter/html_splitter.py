import re
from html.parser import HTMLParser

MAX_LENGTH = 4096


class HTMLTagTracker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.open_tags = []

    def handle_starttag(self, tag, attrs):
        # saving tags
        if tag in ("b", "i", "u", "s", "code", "pre", "a", "span", "blockquote"):
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
    # language-aware: <pre><code class="language-python">...</code></pre>
    match = re.match(r"<pre><code(.*?)>(.*)</code></pre>", pre_block, re.DOTALL)
    if match:
        attr, content = match.groups()
        lines = content.splitlines(keepends=True)
        chunks, buf = [], ""
        for line in lines:
            if len(buf) + len(line) + len('<pre><code></code></pre>') > max_length:
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
        for line in lines:
            if len(buf) + len(line) + len('<pre></pre>') > max_length:
                chunks.append(f"<pre>{buf}</pre>")
                buf = ""
            buf += line
        if buf:
            chunks.append(f"<pre>{buf}</pre>")
        return chunks


def split_html_for_telegram(text: str, trim_leading_newlines = False, max_length = MAX_LENGTH) -> list[str]:
    chunks = []
    pattern = re.compile(r"(<pre>.*?</pre>|<pre><code.*?</code></pre>)", re.DOTALL)
    parts = pattern.split(text)

    for part in parts:
        if not part:
            continue
        if part.startswith("<pre>") or part.startswith("<pre><code"):
            pre_chunks = split_pre_block(part, max_length = max_length)
            chunks.extend(pre_chunks)
        else:
            # breaking down regular HTML
            tracker = HTMLTagTracker()
            current = ""
            blocks = re.split(r"(\n\s*\n|<br\s*/?>|\n)", part)
            for block in blocks:
                prospective = current + block
                if len(prospective) > max_length:
                    tracker.feed(current)
                    open_tags = tracker.get_open_tags_html()
                    close_tags = tracker.get_closing_tags_html()
                    chunks.append(open_tags + current + close_tags)
                    current = block
                    tracker = HTMLTagTracker()
                else:
                    current = prospective
            if current.strip():
                tracker.feed(current)
                open_tags = tracker.get_open_tags_html()
                close_tags = tracker.get_closing_tags_html()
                chunks.append(open_tags + current + close_tags)

    # post-unification: combine chunks if they don't exceed the limit in total
    merged_chunks = []
    buf = ""
    for chunk in chunks:

        if len(buf) + len(chunk) <= max_length:
            buf += chunk
        else:
            if buf:
                merged_chunks.append(buf.lstrip("\n") if trim_leading_newlines else buf)
            buf = chunk
    if buf:
        merged_chunks.append(buf.lstrip("\n") if trim_leading_newlines else buf)

    return merged_chunks
