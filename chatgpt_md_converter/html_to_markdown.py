"""Backward-compatible entry point for HTML → Telegram Markdown."""

from .html_markdown.renderer import html_to_telegram_markdown

__all__ = ["html_to_telegram_markdown"]
