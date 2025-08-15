from chatgpt_md_converter.html_splitter import split_html_for_telegram
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