"""DOM-like tree construction for Telegram HTML fragments."""

from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Dict, List, Optional


@dataclass
class Node:
    kind: str  # "text" or "element"
    text: str = ""
    tag: str = ""
    attrs: Dict[str, Optional[str]] = field(default_factory=dict)
    children: List["Node"] = field(default_factory=list)


class _HTMLTreeBuilder(HTMLParser):
    SELF_CLOSING_TAGS = {"br"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.root = Node(kind="element", tag="__root__")
        self._stack: List[Node] = [self.root]

    def handle_starttag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        if tag in self.SELF_CLOSING_TAGS:
            if tag == "br":
                self._stack[-1].children.append(Node(kind="text", text="\n"))
            return
        node = Node(kind="element", tag=tag, attrs=dict(attrs))
        self._stack[-1].children.append(node)
        self._stack.append(node)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self._stack) - 1, 0, -1):
            if self._stack[index].tag == tag:
                del self._stack[index:]
                return

    def handle_startendtag(self, tag: str, attrs: List[tuple[str, Optional[str]]]) -> None:
        if tag in self.SELF_CLOSING_TAGS:
            self.handle_starttag(tag, attrs)
            return
        node = Node(kind="element", tag=tag, attrs=dict(attrs))
        self._stack[-1].children.append(node)

    def handle_data(self, data: str) -> None:
        if data:
            self._stack[-1].children.append(Node(kind="text", text=data))

    def handle_entityref(self, name: str) -> None:
        self.handle_data(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.handle_data(f"&#{name};")


def build_tree(html_text: str) -> List[Node]:
    """Parse HTML and return the list of top-level nodes."""
    builder = _HTMLTreeBuilder()
    builder.feed(html_text)
    builder.close()
    return builder.root.children
