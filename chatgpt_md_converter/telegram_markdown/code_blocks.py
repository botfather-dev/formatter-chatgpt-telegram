"""Code block extraction utilities for Telegram Markdown conversion."""

import re

from .html_escape import escape_code_content

_CODE_BLOCK_RE = re.compile(
    r"(?P<fence>`{3,})(?P<lang>\w+)?\n?[\s\S]*?(?<=\n)?(?P=fence)",
    flags=re.DOTALL,
)



def _count_unescaped_backticks(text: str) -> int:
    """Return the number of backticks not escaped by a backslash."""
    count = 0
    for index, char in enumerate(text):
        if char != "`":
            continue
        backslashes = 0
        j = index - 1
        while j >= 0 and text[j] == '\\':
            backslashes += 1
            j -= 1
        if backslashes % 2 == 0:
            count += 1
    return count

def ensure_closing_delimiters(text: str) -> str:
    """Append any missing closing backtick fences for Markdown code blocks."""
    open_fence = None
    for line in text.splitlines():
        stripped = line.strip()
        if open_fence is None:
            match = re.match(r"^(?P<fence>`{3,})(?P<lang>\w+)?$", stripped)
            if match:
                open_fence = match.group("fence")
        else:
            if stripped.endswith(open_fence):
                open_fence = None

    if open_fence is not None:
        if not text.endswith("\n"):
            text += "\n"
        text += open_fence

    cleaned_inline = _CODE_BLOCK_RE.sub("", text)
    if cleaned_inline.count("```") % 2 != 0:
        text += "```"

    cleaned_inline = _CODE_BLOCK_RE.sub("", text)
    if _count_unescaped_backticks(cleaned_inline) % 2 != 0:
        text += "`"

    return text


def extract_and_convert_code_blocks(text: str):
    """Replace fenced code blocks with placeholders and return HTML renderings."""
    text = ensure_closing_delimiters(text)
    placeholders: list[str] = []
    code_blocks: dict[str, str] = {}

    def _replacement(match: re.Match[str]) -> tuple[str, str]:
        language = match.group("lang") or ""
        code_content = match.group("code")
        escaped = escape_code_content(code_content)
        placeholder = f"CODEBLOCKPLACEHOLDER_{len(placeholders)}_"
        placeholders.append(placeholder)
        if language:
            html_block = f'<pre><code class="language-{language}">{escaped}</code></pre>'
        else:
            html_block = f"<pre><code>{escaped}</code></pre>"
        return placeholder, html_block

    modified = text
    pattern = re.compile(
        r"(?P<fence>`{3,})(?P<lang>\w+)?\n?(?P<code>[\s\S]*?)(?<=\n)?(?P=fence)",
        flags=re.DOTALL,
    )
    for match in pattern.finditer(text):
        placeholder, html_block = _replacement(match)
        code_blocks[placeholder] = html_block
        modified = modified.replace(match.group(0), placeholder, 1)

    return modified, code_blocks


def reinsert_code_blocks(text: str, code_blocks: dict[str, str]) -> str:
    """Insert rendered HTML code blocks back into their placeholders."""
    for placeholder, html_block in code_blocks.items():
        text = text.replace(placeholder, html_block, 1)
    return text
