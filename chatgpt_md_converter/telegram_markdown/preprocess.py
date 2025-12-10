"""Pre-processing helpers for Telegram Markdown conversion."""


def combine_blockquotes(text: str) -> str:
    """Collapse consecutive Markdown blockquote lines into Telegram HTML blocks."""
    lines = text.split("\n")
    combined_lines = []
    blockquote_lines = []
    in_blockquote = False
    is_expandable = False

    for line in lines:
        if line.startswith("**>"):
            in_blockquote = True
            is_expandable = True
            blockquote_lines.append(line[3:].strip())
        elif line.startswith(">**") and (len(line) == 3 or line[3].isspace()):
            in_blockquote = True
            is_expandable = True
            blockquote_lines.append(line[3:].strip())
        elif line.startswith(">"):
            if not in_blockquote:
                in_blockquote = True
                is_expandable = False
            blockquote_lines.append(line[1:].strip())
        else:
            if in_blockquote:
                combined_lines.append(_render_blockquote(blockquote_lines, is_expandable))
                blockquote_lines = []
                in_blockquote = False
                is_expandable = False
            combined_lines.append(line)

    if in_blockquote:
        combined_lines.append(_render_blockquote(blockquote_lines, is_expandable))

    return "\n".join(combined_lines)


def _render_blockquote(lines: list[str], expandable: bool) -> str:
    if expandable:
        return "<blockquote expandable>" + "\n".join(lines) + "</blockquote>"
    return "<blockquote>" + "\n".join(lines) + "</blockquote>"
