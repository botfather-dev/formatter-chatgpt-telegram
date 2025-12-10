
import pytest

from chatgpt_md_converter import html_to_telegram_markdown, telegram_format
from tests.fixtures.markdown_roundtrips import ROUND_TRIP_CASES


@pytest.mark.parametrize("_case, markdown_input, expected_markdown", ROUND_TRIP_CASES)
def test_html_round_trip_normalizes_markdown(_case, markdown_input, expected_markdown):
    html1 = telegram_format(markdown_input)
    markdown2 = html_to_telegram_markdown(html1)
    html2 = telegram_format(markdown2)
    markdown3 = html_to_telegram_markdown(html2)
    html3 = telegram_format(markdown3)

    assert markdown2 == expected_markdown
    assert markdown3 == expected_markdown
    assert html1 == html2 == html3
    assert '<br' not in html1
    assert '<br' not in html2
    assert '<br' not in html3


@pytest.mark.parametrize("_case, markdown_input, _", ROUND_TRIP_CASES)
def test_markdown_html_markdown_cycle_is_idempotent(_case, markdown_input, _):
    html_first = telegram_format(markdown_input)
    markdown_second = html_to_telegram_markdown(html_first)
    html_third = telegram_format(markdown_second)

    assert '<br' not in html_first
    assert '<br' not in html_third
    assert html_first == html_third


def test_html_to_markdown_expandable_blockquote():
    html_text = "<blockquote expandable>заголовок\nрядок 2\nрядок 3</blockquote>"
    expected_markdown = ">** заголовок\n> рядок 2\n> рядок 3"
    markdown = html_to_telegram_markdown(html_text)
    assert markdown == expected_markdown
