import pytest
from chatgpt_md_converter.html_splitter import MIN_LENGTH, split_html_for_telegram
from .html_examples import *
import re

def test_html_splitter():
    chunks = split_html_for_telegram(input_text)
    valid_chunks = [valid_chunk_1, valid_chunk_2, valid_chunk_3]
    for index, chunk in enumerate(chunks):
        assert chunk == valid_chunks[index], (
            f"expected: \n\n{valid_chunks[index]} \n\n got: \n\n{chunk}"
        )

def test_html_splitter__remove_leading_brakes():
    chunks = split_html_for_telegram(input_text, trim_empty_leadming_lines=True)
    valid_chunks = [valid_chunk_1, valid_chunk_2, valid_chunk_3_remove_leading_brakes]
    for index, chunk in enumerate(chunks):
        assert chunk == valid_chunks[index], (
            f"expected: \n\n{valid_chunks[index]} \n\n got: \n\n{chunk}"
        )

def test_html_splitter_max_length_550():
    chunks = split_html_for_telegram(
        long_code_input, max_length=550, trim_empty_leadming_lines=True
    )

    def load_expected_chunks_550():
      raw = re.split(r"END\n?", expected_550)
      chunks = []
      for part in raw:
          if not part.strip():
              continue
          lines = part.splitlines()
          chunks.append("\n".join(lines[1:]))
      return chunks

    valid_chunks = load_expected_chunks_550()
    for index, chunk in enumerate(chunks):
        assert chunk == valid_chunks[index], (
            f"expected: \n\n{valid_chunks[index]} \n\n got: \n\n{chunk}"
        )
        assert len(chunk) <= 550

def test_split_html_respects_max_length_by_words():
    text = "<b>" + "<i>word</i> " * 100 + "</b>"
    chunks = split_html_for_telegram(text, max_length=550)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 550
        assert chunk.startswith("<b>")
        assert chunk.endswith("</b>")
        assert chunk.count("<i>") == chunk.count("</i>")


def test_split_html_only_tags_raises():
    text = "<b></b>" * 200
    with pytest.raises(ValueError):
        split_html_for_telegram(text, max_length=600)


def test_split_html_min_length_enforced():
    with pytest.raises(ValueError):
        split_html_for_telegram("hello", max_length=MIN_LENGTH - 1)


LONG_TEXT = "<b><i>" + "word " * 96 + "word!" + "</i></b>"

SHORT_TEXT = "<u>" + "another " * 9 + "another" + "</u>"


def test_split_html_keeps_newline_without_trim():
    text = LONG_TEXT + "\n\n" + SHORT_TEXT
    chunks = split_html_for_telegram(text, max_length=500, trim_empty_leadming_lines=False)
    assert chunks[0] == LONG_TEXT
    assert chunks[1].startswith("\n")
    assert chunks[1].endswith(SHORT_TEXT)
    assert chunks[1].lstrip("\n").startswith("<u>")
    assert chunks[1].lstrip("\n").endswith("</u>")


def test_split_html_trims_leading_newline_on_new_chunk():
    text = LONG_TEXT + "\n\n" + SHORT_TEXT
    chunks = split_html_for_telegram(text, max_length=500, trim_empty_leadming_lines=True)
    assert chunks == [LONG_TEXT, SHORT_TEXT]