import pytest

from chatgpt_md_converter import html_to_telegram_markdown


@pytest.mark.parametrize(
    ("html", "expected"),
    [
        ("Start <b>bold </b>finish", "Start **bold** finish"),
        ("Start <b> bold</b> finish", "Start  **bold** finish"),
        ("Start <i> italics </i>finish", "Start  _italics_ finish"),
        ("Start <i>value_</i>end", "Start *value_*end"),
        ("Start <u> underline </u>finish", "Start  __underline__ finish"),
        (
            "Start <span class=\"tg-spoiler\"> secret </span>end",
            "Start  ||secret|| end",
        ),
        (
            "Intro <b>bold <i> inner </i> block</b> outro",
            "Intro **bold  _inner_  block** outro",
        ),
    ],
)
def test_html_to_markdown_strips_inline_whitespace(html: str, expected: str) -> None:
    assert html_to_telegram_markdown(html) == expected
