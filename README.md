# ChatGPT Markdown to Telegram HTML Parser

## Overview

This project provides a solution for converting Telegram-style Markdown formatted text into HTML markup supported by the Telegram Bot API, specifically tailored for use in ChatGPT bots developed with the OpenAI API. It includes features for handling various Markdown elements and ensures proper tag closure, making it suitable for streaming mode applications.

## Features

- Converts Telegram-style Markdown syntax to Telegram-compatible HTML
- Supports text styling:
  - Bold: `**text**` → `<b>text</b>`
  - Italic: `*text*` or `_text_` → `<i>text</i>`
  - Underline: `__text__` → `<u>text</u>`
  - Strikethrough: `~~text~~` → `<s>text</s>`
  - Spoiler: `||text||` → `<span class="tg-spoiler">text</span>`
  - Inline code: `` `code` `` → `<code>code</code>`
- Handles nested text styling
- Converts links: `[text](URL)` → `<a href="URL">text</a>`
- Processes code blocks with language specification
- Supports blockquotes:
  - Regular blockquotes: `> text` → `<blockquote>text</blockquote>`
  - Expandable blockquotes: `**> text` → `<blockquote expandable>text</blockquote>`
- Automatically appends missing closing delimiters for code blocks
- Escapes HTML special characters to prevent unwanted HTML rendering

## Usage

To use the Markdown to Telegram HTML Parser in your ChatGPT bot, integrate the provided Python functions into your bot's processing pipeline. Here is a brief overview of how to incorporate the parser:

1. **Ensure Closing Delimiters**: Automatically appends missing closing delimiters for backticks to ensure proper parsing.

2. **Extract and Convert Code Blocks**: Extracts Markdown code blocks, converts them to HTML `<pre><code>` format, and replaces them with placeholders to prevent formatting within code blocks.

3. **Markdown to HTML Conversion**: Applies various regex substitutions and custom logic to convert supported Markdown formatting to Telegram-compatible HTML tags.

4. **Reinsert Code Blocks**: Reinserts the previously extracted and converted code blocks back into the main text, replacing placeholders with the appropriate HTML content.

Simply call the `telegram_format(text: str) -> str` function with your Markdown-formatted text as input to receive the converted HTML output ready for use with the Telegram Bot API.

## Installation

```sh
pip install chatgpt-md-converter
```

## Example

```python
from chatgpt_md_converter import telegram_format

# Basic formatting example
text = """
Here is some **bold**, __underline__, and `inline code`.
This is a ||spoiler text|| and *italic*.

Code example:
print('Hello, world!')
"""

# Blockquotes example
blockquote_text = """
> Regular blockquote
> Multiple lines

**> Expandable blockquote
> Hidden by default
> Multiple lines
"""

formatted_text = telegram_format(text)
formatted_blockquote = telegram_format(blockquote_text)

print(formatted_text)
print(formatted_blockquote)
```

### Output:

```
Here is some <b>bold</b>, <u>underline</u>, and <code>inline code</code>.
This is a <span class="tg-spoiler">spoiler text</span> and <i>italic</i>.

Code example:
print('Hello, world!')

<blockquote>Regular blockquote
Multiple lines</blockquote>

<blockquote expandable>Expandable blockquote
Hidden by default
Multiple lines</blockquote>
```

## Requirements

- Python 3.x
- No external libraries required (uses built-in `re` module for regex operations)

## Contribution

Feel free to contribute to this project by submitting pull requests or opening issues for bugs, feature requests, or improvements.

## Prompting LLMs for Telegram-Specific Formatting

> **Note**:
> Since standard Markdown doesn't include Telegram-specific features like spoilers (`||text||`) and expandable blockquotes (`**> text`), you'll need to explicitly instruct LLMs to use these formats. Here's a suggested prompt addition to include in your system message or initial instructions:

````
When formatting your responses for Telegram, please use these special formatting conventions:

1. For content that should be hidden as a spoiler (revealed only when users click):
   Use: ||spoiler content here||
   Example: This is visible, but ||this is hidden until clicked||.

2. For lengthy explanations or optional content that should be collapsed:
   Use: **> Expandable section title

   > Content line 1
   > Content line 2
   > (Each line of the expandable blockquote should start with ">")

3. Continue using standard markdown for other formatting:
   - **bold text**
   - *italic text*
   - __underlined text__
   - ~~strikethrough~~
   - `inline code`
   - ```code blocks```
   - [link text](URL)

Apply spoilers for:

- Solution reveals
- Potential plot spoilers
- Sensitive information
- Surprising facts

Use expandable blockquotes for:

- Detailed explanations
- Long examples
- Optional reading
- Technical details
- Additional context not needed by all users
````

You can add this prompt to your system message when initializing your ChatGPT interactions to ensure the model properly formats content for optimal display in Telegram.
