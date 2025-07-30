import re


def ensure_closing_delimiters(text: str) -> str:
    """Append missing closing backtick delimiters."""

    code_block_re = re.compile(
        r"(?P<fence>`{3,})(?P<lang>\w+)?\n?[\s\S]*?(?<=\n)?(?P=fence)",
        flags=re.DOTALL,
    )

    # Remove complete code blocks from consideration so inner backticks
    # don't affect delimiter balancing.
    cleaned = code_block_re.sub("", text)

    # Detect unclosed fences by tracking opening fence lengths.
    stack = []
    for line in cleaned.splitlines():
        m = re.match(r"^(?P<fence>`{3,})(?P<lang>\w+)?$", line.strip())
        if not m:
            continue
        fence = m.group("fence")
        if stack and fence == stack[-1]:
            stack.pop()
        else:
            stack.append(fence)

    if stack:
        text += "\n" + stack[-1]

    cleaned_inline = code_block_re.sub("", text)

    # Balance triple backticks that are not part of a complete fence.
    if cleaned_inline.count("```") % 2 != 0:
        text += "```"

    # Balance single backticks outside fenced blocks.
    cleaned_inline = code_block_re.sub("", text)
    if cleaned_inline.count("`") % 2 != 0:
        text += "`"

    return text


def extract_and_convert_code_blocks(text: str):
    """
    Extracts code blocks from the text, converting them to HTML <pre><code> format,
    and replaces them with placeholders. Also ensures closing delimiters for unmatched blocks.
    """
    text = ensure_closing_delimiters(text)
    placeholders = []
    code_blocks = {}

    def replacer(match):
        language = match.group("lang") if match.group("lang") else ""
        code_content = match.group("code")

        # Properly escape HTML entities in code content
        escaped_content = (
            code_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )

        placeholder = f"CODEBLOCKPLACEHOLDER{len(placeholders)}"
        placeholders.append(placeholder)
        if not language:
            html_code_block = f"<pre><code>{escaped_content}</code></pre>"
        else:
            html_code_block = (
                f'<pre><code class="language-{language}">{escaped_content}</code></pre>'
            )
        return (placeholder, html_code_block)

    modified_text = text
    code_block_pattern = re.compile(
        r"(?P<fence>`{3,})(?P<lang>\w+)?\n?(?P<code>[\s\S]*?)(?<=\n)?(?P=fence)",
        flags=re.DOTALL,
    )
    for match in code_block_pattern.finditer(text):
        placeholder, html_code_block = replacer(
            match
        )
        code_blocks[placeholder] = html_code_block
        modified_text = modified_text.replace(match.group(0), placeholder, 1)

    return modified_text, code_blocks


def reinsert_code_blocks(text: str, code_blocks: dict) -> str:
    """
    Reinserts HTML code blocks into the text, replacing their placeholders.
    """
    for placeholder, html_code_block in code_blocks.items():
        text = text.replace(placeholder, html_code_block, 1)
    return text
