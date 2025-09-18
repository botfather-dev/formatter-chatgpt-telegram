"""Rendering state for HTML → Telegram Markdown conversion."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RenderState:
    bold_depth: int = 0
    italic_depth: int = 0

    def child(self, **updates: int) -> "RenderState":
        data = {"bold_depth": self.bold_depth, "italic_depth": self.italic_depth}
        data.update(updates)
        return RenderState(**data)
