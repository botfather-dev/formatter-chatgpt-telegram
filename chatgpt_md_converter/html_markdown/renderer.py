"""High-level HTML → Telegram Markdown renderer."""

from __future__ import annotations

from typing import List

from .escaping import post_process
from .handlers import render_nodes
from .state import RenderState
from .tree import Node, build_tree


def html_to_telegram_markdown(html_text: str) -> str:
    nodes: List[Node] = build_tree(html_text)
    markdown = render_nodes(nodes, RenderState())
    return post_process(markdown)
