"""Tag-specific renderers for Telegram Markdown."""

from __future__ import annotations

from typing import Callable, Dict

from .escaping import (collect_text, escape_inline_code, escape_link_label,
                       escape_link_url, normalise_text)
from .state import RenderState
from .tree import Node

InlineHandler = Callable[[Node, RenderState], str]


_INLINE_MARKERS: Dict[str, tuple[str, str]] = {
    "u": ("__", "__"),
    "ins": ("__", "__"),
    "s": ("~~", "~~"),
    "strike": ("~~", "~~"),
    "del": ("~~", "~~"),
}


def render_nodes(nodes: list[Node], state: RenderState) -> str:
    return "".join(render_node(node, state) for node in nodes)


def render_node(node: Node, state: RenderState) -> str:
    if node.kind == "text":
        return normalise_text(node.text)

    handler = TAG_DISPATCH.get(node.tag.lower())
    if handler:
        return handler(node, state)
    return render_nodes(node.children, state)


def _split_surrounding_whitespace(text: str) -> tuple[str, str, str]:
    """Return leading whitespace, core text, and trailing whitespace."""

    start = 0
    end = len(text)

    while start < end and text[start].isspace():
        start += 1

    while end > start and text[end - 1].isspace():
        end -= 1

    return text[:start], text[start:end], text[end:]


def _italic_boundary_conflict(marker: str, core: str) -> bool:
    if marker == "*":
        return core.startswith("*") or core.endswith("*")

    if marker == "_":
        starts = core.startswith("_")
        if starts and len(core) > 1 and core[1] == "_":
            starts = False

        ends = core.endswith("_")
        if ends and len(core) > 1 and core[-2] == "_":
            ends = False

        return starts or ends

    return False


def _choose_italic_marker(state: RenderState, core: str) -> str:
    depth = state.italic_depth

    if state.bold_depth > 0 and depth == 0:
        candidates = ["_", "*"]
    elif depth % 2 == 0:
        candidates = ["*", "_"]
    else:
        candidates = ["_", "*"]

    for marker in candidates:
        if not _italic_boundary_conflict(marker, core):
            return marker

    return candidates[0]


def _handle_bold(node: Node, state: RenderState) -> str:
    inner_state = state.child(bold_depth=state.bold_depth + 1)
    inner = render_nodes(node.children, inner_state)
    leading, core, trailing = _split_surrounding_whitespace(inner)
    if not core:
        return leading + trailing
    return f"{leading}**{core}**{trailing}"


def _handle_italic(node: Node, state: RenderState) -> str:
    depth = state.italic_depth
    inner_state = state.child(italic_depth=depth + 1)
    inner = render_nodes(node.children, inner_state)
    leading, core, trailing = _split_surrounding_whitespace(inner)
    if not core:
        return leading + trailing
    marker = _choose_italic_marker(state, core)
    return f"{leading}{marker}{core}{marker}{trailing}"


def _handle_inline_marker(node: Node, state: RenderState) -> str:
    marker_open, marker_close = _INLINE_MARKERS[node.tag.lower()]
    inner = render_nodes(node.children, state)
    leading, core, trailing = _split_surrounding_whitespace(inner)
    if not core:
        return leading + trailing
    return f"{leading}{marker_open}{core}{marker_close}{trailing}"


def _handle_spoiler(node: Node, state: RenderState) -> str:
    inner = render_nodes(node.children, state)
    leading, core, trailing = _split_surrounding_whitespace(inner)
    if not core:
        return leading + trailing
    return f"{leading}||{core}||{trailing}"


def _handle_code(node: Node, state: RenderState) -> str:
    inner = collect_text(node)
    return f"`{escape_inline_code(inner)}`"


def _handle_pre(node: Node, state: RenderState) -> str:
    children = node.children
    language: str | None = None
    content_node: Node

    if len(children) == 1 and children[0].kind == "element" and children[0].tag.lower() == "code":
        content_node = children[0]
        class_attr = content_node.attrs.get("class") or ""
        for part in class_attr.split():
            if part.startswith("language-"):
                language = part.split("-", 1)[1]
                break
    else:
        content_node = Node(kind="element", tag="__virtual__", children=children)

    inner_text = collect_text(content_node)
    fence = f"```{language}" if language else "```"
    if language or "\n" in inner_text:
        return f"{fence}\n{inner_text}```"
    return f"{fence}{inner_text}```"


def _handle_link(node: Node, state: RenderState) -> str:
    href = node.attrs.get("href", "") or ""
    label = render_nodes(node.children, state)
    if not label:
        label = href

    escaped_label = escape_link_label(label)
    escaped_url = escape_link_url(href)

    if href.startswith("tg://emoji?"):
        return f"![{escaped_label}]({escaped_url})"
    return f"[{escaped_label}]({escaped_url})"


def _handle_blockquote(node: Node, state: RenderState) -> str:
    inner = render_nodes(node.children, state)
    lines = inner.split("\n")
    expandable = "expandable" in node.attrs
    rendered: list[str] = []
    for index, line in enumerate(lines):
        stripped = line.rstrip("\r")
        if expandable:
            marker = ">**" if index == 0 else ">"
            rendered.append(f"{marker} {stripped}" if stripped else marker)
        else:
            prefix = ">"
            rendered.append(f"{prefix} {stripped}" if stripped else prefix)
    return "\n".join(rendered)


def _handle_tg_emoji(node: Node, state: RenderState) -> str:
    emoji_id = node.attrs.get("emoji-id")
    label = render_nodes(node.children, state)
    if emoji_id:
        href = f"tg://emoji?id={emoji_id}"
        return f"![{escape_link_label(label)}]({href})"
    return label


def _handle_span(node: Node, state: RenderState) -> str:
    classes = (node.attrs.get("class") or "").split()
    if any(cls == "tg-spoiler" for cls in classes):
        return _handle_spoiler(node, state)
    if any(cls == "tg-emoji" for cls in classes):
        return render_nodes(node.children, state)
    return render_nodes(node.children, state)


TAG_DISPATCH: Dict[str, Callable[[Node, RenderState], str]] = {
    "b": _handle_bold,
    "strong": _handle_bold,
    "i": _handle_italic,
    "em": _handle_italic,
    "u": _handle_inline_marker,
    "ins": _handle_inline_marker,
    "s": _handle_inline_marker,
    "strike": _handle_inline_marker,
    "del": _handle_inline_marker,
    "span": _handle_span,
    "tg-spoiler": _handle_spoiler,
    "code": _handle_code,
    "pre": _handle_pre,
    "a": _handle_link,
    "blockquote": _handle_blockquote,
    "tg-emoji": _handle_tg_emoji,
}
