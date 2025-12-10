"""Round-trip Markdown ↔ HTML test cases."""

import textwrap

ROUND_TRIP_CASES = [
    # Inline formatting -------------------------------------------------
    (
        "basic_formatting",
        "Hello, **bold** _italic_ __underline__ ~~strike~~ ||spoiler||"
        " [link](http://example.com) and [user](tg://user?id=123456789) with `code`",
        "Hello, **bold** _italic_ __underline__ ~~strike~~ ||spoiler||"
        " [link](http://example.com) and [user](tg://user?id=123456789) with `code`",
    ),
    (
        "nested_inline",
        "*bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*",
        "*bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*",
    ),
    # Block-level structures --------------------------------------------
    (
        "blocks_lists_code",
        textwrap.dedent(
            """
            > Block quotation started
            > Block quotation continued

            >** Expandable block quotation started
            > Expandable block quotation continued
            > Hidden by default||

            - Bullet with `code`
            - Second bullet with __underline__ and ||spoiler||

            ```python
            for i in range(2):
                print(i)
            ```
            """
        ).strip(),
        textwrap.dedent(
            """
            > Block quotation started
            > Block quotation continued

            >** Expandable block quotation started
            > Expandable block quotation continued
            > Hidden by default||

            - Bullet with `code`
            - Second bullet with __underline__ and ||spoiler||

            ```python
            for i in range(2):
                print(i)
            ```
            """
        ).strip(),
    ),
    (
        "emoji_and_links",
        "![👍](tg://emoji?id=5368324170671202286) **bold** [inline](https://example.org?q=1&v=2)",
        "![👍](tg://emoji?id=5368324170671202286) **bold** [inline](https://example.org?q=1&v=2)",
    ),
    (
        "combination_of_markdown_elements",
        textwrap.dedent(
            """
            # Heading
            This is a test of **bold**, __underline__, and `inline code`.
            - Item 1
            * Item 2

            ```python
            for i in range(3):
                print(i)
            ```

            [Link](http://example.com)
            """
        ).strip(),
        textwrap.dedent(
            """
            **Heading**
            This is a test of **bold**, __underline__, and `inline code`.
            - Item 1
            - Item 2

            ```python
            for i in range(3):
                print(i)
            ```

            [Link](http://example.com)
            """
        ).strip(),
    ),
    (
        "heading_and_lists",
        textwrap.dedent(
            """
            # Heading Example
            * First bullet
            - Second bullet with **bold**
            """
        ).strip(),
        textwrap.dedent(
            """
            **Heading Example**
            - First bullet
            - Second bullet with **bold**
            """
        ).strip(),
    ),
    # Code blocks -------------------------------------------------------
    (
        "inline_code_escaping",
        "Escaped \\*asterisks\\* and `code with \\` backtick`",
        "Escaped \\*asterisks\\* and `code with \\` backtick`",
    ),
    (
        "standalone_pre_block",
        textwrap.dedent(
            """
            ```
            plain code block
            with <tags> & ampersand
            ```
            """
        ).strip(),
        textwrap.dedent(
            """
            ```
            plain code block
            with <tags> & ampersand
            ```
            """
        ).strip(),
    ),
    (
        "language_pre_block",
        textwrap.dedent(
            """
            ```javascript
            const url = "https://example.com?q=1&v=2";
            console.log(url);
            ```
            """
        ).strip(),
        textwrap.dedent(
            """
            ```javascript
            const url = "https://example.com?q=1&v=2";
            console.log(url);
            ```
            """
        ).strip(),
    ),
    # Quotations and spacing -------------------------------------------
    (
        "blockquote_with_blank_lines",
        textwrap.dedent(
            """
            > First quote line
            >
            > Third quote line
            """
        ).strip(),
        textwrap.dedent(
            """
            > First quote line
            >
            > Third quote line
            """
        ).strip(),
    ),
    (
        "expandable_blockquote_marker",
        textwrap.dedent(
            """
            >** заголовок довгої цитати
            > рядок 2
            > рядок 3
            > рядок 4
            > і ще хоч сто рядків
            """
        ).strip(),
        textwrap.dedent(
            """
            >** заголовок довгої цитати
            > рядок 2
            > рядок 3
            > рядок 4
            > і ще хоч сто рядків
            """
        ).strip(),
    ),
    # Simple emphasis normalisation ------------------------------------
    (
        "bold_only",
        "This is **bold** text",
        "This is **bold** text",
    ),
    (
        "italic_underscore",
        "This is _italic_ text",
        "This is _italic_ text",
    ),
    (
        "italic_star",
        "This is *italic* text",
        "This is _italic_ text",
    ),
    (
        "bold_and_underline_combo",
        "This is **bold** and this is __underline__.",
        "This is **bold** and this is __underline__.",
    ),
    (
        "nested_markdown_syntax",
        "This is **bold and _italic_** text.",
        "This is **bold and _italic_** text.",
    ),
    (
        "nested_bold_within_italic",
        "This is *__bold within italic__* text.",
        "This is *__bold within italic__* text.",
    ),
    (
        "italic_within_bold",
        "This is **bold and _italic_ together**.",
        "This is **bold and _italic_ together**.",
    ),
    # Mixed constructs --------------------------------------------------
    (
        "escape_angle_brackets",
        "Avoid using < or > in your HTML.",
        "Avoid using < or > in your HTML.",
    ),
    (
        "inline_code_within_bold_text",
        "This is **bold and `inline code` together**.",
        "This is **bold and `inline code` together**.",
    ),
    (
        "mixed_formatting_lists_links",
        textwrap.dedent(
            """
            - This is a list item with **bold**, __underline__, and [a link](http://example.com)
            - Another item with ***bold and italic*** text
            """
        ).strip(),
        textwrap.dedent(
            """
            - This is a list item with **bold**, __underline__, and [a link](http://example.com)
            - Another item with **_bold and italic_** text
            """
        ).strip(),
    ),
    (
        "special_characters_code_block",
        "Here is a code block: ```<script>alert('Hello')</script>```",
        "Here is a code block: ```<script>alert('Hello')</script>```",
    ),
    (
        "code_block_within_bold",
        "This is **bold with a `code block` inside**.",
        "This is **bold with a `code block` inside**.",
    ),
    (
        "triple_backticks_nested_markdown",
        "```python\n**bold text** and __underline__ in code block```",
        "```python\n**bold text** and __underline__ in code block```",
    ),
    (
        "unmatched_code_delimiter",
        "This has an `unmatched code delimiter.",
        "This has an `unmatched code delimiter.`",
    ),
    (
        "vector_storage_trim",
        "- List item with `code`\n* Another `code` item 【reference】",
        textwrap.dedent(
            """
            - List item with `code`
            - Another `code` item
            """
        ).strip(),
    ),
    (
        "inline_code_within_lists",
        "- List item with `code`\n- Another `code` item",
        "- List item with `code`\n- Another `code` item",
    ),
    (
        "strikethrough",
        "This is ~~strikethrough~~ text.",
        "This is ~~strikethrough~~ text.",
    ),
    (
        "preformatted_block_with_unusual_language",
        "```weirdLang\nSome weirdLang code\n```",
        "```weirdLang\nSome weirdLang code\n```",
    ),
]
