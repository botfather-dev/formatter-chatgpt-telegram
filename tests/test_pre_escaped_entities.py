"""Tests for handling pre-escaped HTML entities from LLMs.

LLMs sometimes output &lt; &gt; &amp; instead of < > & in markdown code
blocks and inline code. The formatter should normalize these to avoid
double-escaping (e.g. &amp;lt; in the final HTML).
"""

import pytest

from chatgpt_md_converter import html_to_telegram_markdown, telegram_format


class TestInlineCodePreEscaped:
    """Inline code with pre-escaped HTML entities."""

    def test_pre_escaped_angle_brackets(self):
        # LLM wrote &lt; instead of < in inline code
        md_escaped = "Use `&lt;tg-emoji emoji-id=\"ID\"&gt;⭐&lt;/tg-emoji&gt;` for custom emoji"
        md_correct = 'Use `<tg-emoji emoji-id="ID">⭐</tg-emoji>` for custom emoji'

        html_escaped = telegram_format(md_escaped)
        html_correct = telegram_format(md_correct)

        assert html_escaped == html_correct
        assert "&amp;lt;" not in html_escaped
        assert "&lt;tg-emoji" in html_escaped  # single escape only

    def test_pre_escaped_ampersand(self):
        md_escaped = "Query: `a &amp; b`"
        md_correct = "Query: `a & b`"

        html_escaped = telegram_format(md_escaped)
        html_correct = telegram_format(md_correct)

        assert html_escaped == html_correct
        assert "&amp;amp;" not in html_escaped

    def test_pre_escaped_mixed(self):
        md_escaped = "`&lt;div class=&quot;test&quot;&gt;hello&lt;/div&gt;`"
        md_correct = '`<div class="test">hello</div>`'

        html_escaped = telegram_format(md_escaped)
        html_correct = telegram_format(md_correct)

        assert html_escaped == html_correct

    def test_no_double_escaping_gt_lt(self):
        md = "`x &lt; y &gt; z`"
        html = telegram_format(md)

        assert "&amp;lt;" not in html
        assert "&amp;gt;" not in html
        assert "<code>x &lt; y &gt; z</code>" in html


class TestCodeBlockPreEscaped:
    """Fenced code blocks with pre-escaped HTML entities."""

    def test_pre_escaped_html_code_block(self):
        md_escaped = "```html\n&lt;tg-emoji emoji-id=\"ID\"&gt;⭐&lt;/tg-emoji&gt;\n```"
        md_correct = '```html\n<tg-emoji emoji-id="ID">⭐</tg-emoji>\n```'

        html_escaped = telegram_format(md_escaped)
        html_correct = telegram_format(md_correct)

        assert html_escaped == html_correct
        assert "&amp;lt;" not in html_escaped

    def test_pre_escaped_ampersand_code_block(self):
        md_escaped = "```\na &amp; b\n```"
        md_correct = "```\na & b\n```"

        html_escaped = telegram_format(md_escaped)
        html_correct = telegram_format(md_correct)

        assert html_escaped == html_correct

    def test_pre_escaped_mixed_code_block(self):
        md_escaped = "```xml\n&lt;root attr=&quot;val&quot;&gt;\n  &lt;child/&gt;\n&lt;/root&gt;\n```"
        md_correct = '```xml\n<root attr="val">\n  <child/>\n</root>\n```'

        html_escaped = telegram_format(md_escaped)
        html_correct = telegram_format(md_correct)

        assert html_escaped == html_correct


class TestRoundTripPreEscaped:
    """Round-trip: pre-escaped input should normalize to the same as clean input."""

    def test_inline_code_round_trip(self):
        md_escaped = "Use `&lt;b&gt;bold&lt;/b&gt;` tag"
        md_correct = "Use `<b>bold</b>` tag"

        html1 = telegram_format(md_escaped)
        md1 = html_to_telegram_markdown(html1)
        html2 = telegram_format(md1)

        html_ref = telegram_format(md_correct)
        md_ref = html_to_telegram_markdown(html_ref)

        # After one round-trip, both should converge
        assert md1 == md_ref
        assert html1 == html_ref
        assert html2 == html_ref

    def test_code_block_round_trip(self):
        md_escaped = "```\n&lt;div&gt;test&lt;/div&gt;\n```"
        md_correct = "```\n<div>test</div>\n```"

        html1 = telegram_format(md_escaped)
        md1 = html_to_telegram_markdown(html1)
        html2 = telegram_format(md1)

        html_ref = telegram_format(md_correct)
        md_ref = html_to_telegram_markdown(html_ref)

        assert md1 == md_ref
        assert html1 == html_ref
        assert html2 == html_ref

    def test_real_world_tg_emoji_case(self):
        """The exact scenario from production: LLM pre-escapes tg-emoji tags."""
        md_input = (
            "В `input_message_content` ти віддаєш _готовий текст_:\n"
            "- HTML: `&lt;tg-emoji emoji-id=\"ID\"&gt;⭐&lt;/tg-emoji&gt;`\n"
            "- MarkdownV2: `![⭐](tg://emoji?id=ID)`"
        )
        html = telegram_format(md_input)

        # Should NOT have double-escaped entities
        assert "&amp;lt;" not in html
        assert "&amp;gt;" not in html

        # Should have proper single-escaped entities in <code> tags
        assert '<code>&lt;tg-emoji emoji-id="ID"&gt;⭐&lt;/tg-emoji&gt;</code>' in html

        # Round-trip should be stable
        md_back = html_to_telegram_markdown(html)
        html2 = telegram_format(md_back)
        assert html == html2
