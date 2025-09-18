# split_html_for_telegram highlights

- Import it alongside `telegram_format` and pass your formatted HTML to get Telegram-sized chunks without losing tag structure:
  ```python
  from chatgpt_md_converter import telegram_format, split_html_for_telegram

  html = telegram_format(markdown_text)
  chunks = split_html_for_telegram(html, max_length=1000)
  ```
- Long `<pre><code>` fences are split automatically into multiple fenced messages, so big code blocks stay readable in Telegram.
- Whitespace-free blobs now split cleanly instead of crashing:
  ```python
  split_html_for_telegram("A" * 600, max_length=550)
  # -> ["A" * 550, "A" * 50]
  ```
- Use `trim_empty_leading_lines=True` to drop leading newlines in follow-up messages, and invalid inputs (too-small `max_length` or tag-only content) raise `ValueError` so you can handle them before sending.
