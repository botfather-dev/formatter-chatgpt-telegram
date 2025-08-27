from chatgpt_md_converter.extractors import ensure_closing_delimiters
from chatgpt_md_converter.telegram_formatter import telegram_format


def test_split_by_tag_bold():
    text = "This is **bold** text"
    assert telegram_format(text) == "This is <b>bold</b> text"


def test_telegram_format_italic():
    text = "This is _italic_ text"
    output = telegram_format(text)
    assert output == "This is <i>italic</i> text"


def test_telegram_format_italic_star():
    text = "This is *italic* text"
    output = telegram_format(text)
    assert output == "This is <i>italic</i> text"


def test_triple_backticks_with_language():
    input_text = "```python\nprint('Hello, world!')\n```"
    expected_output = (
        "<pre><code class=\"language-python\">print('Hello, world!')\n</code></pre>"
    )
    output = telegram_format(input_text)
    assert (
        output == expected_output
    ), "Failed converting triple backticks with language to <pre><code> tags"


def test_bold_and_underline_conversion():
    input_text = "This is **bold** and this is __underline__."
    expected_output = "This is <b>bold</b> and this is <u>underline</u>."
    output = telegram_format(input_text)
    assert output == expected_output, "Failed converting ** and __ to <b> and <u> tags"


def test_escaping_special_characters():
    input_text = "Avoid using < or > in your HTML."
    expected_output = "Avoid using &lt; or &gt; in your HTML."
    output = telegram_format(input_text)
    assert output == expected_output, "Failed escaping < and > characters"


def test_nested_markdown_syntax():
    input_text = "This is **bold and _italic_** text."
    expected_output = "This is <b>bold and <i>italic</i></b> text."
    output = telegram_format(input_text)
    assert output == expected_output, "Failed handling nested markdown syntax"


def test_combination_of_markdown_elements():
    input_text = """
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
    expected_output = """
<b>Heading</b>
This is a test of <b>bold</b>, <u>underline</u>, and <code>inline code</code>.
• Item 1
• Item 2

<pre><code class="language-python">for i in range(3):
    print(i)
</code></pre>

<a href="http://example.com">Link</a>
"""
    output = telegram_format(input_text)
    assert (
        output.strip() == expected_output.strip()
    ), "Failed combining multiple markdown elements into HTML"


def test_nested_bold_within_italic():
    input_text = "This is *__bold within italic__* text."
    expected_output = "This is <i><u>bold within italic</u></i> text."
    output = telegram_format(input_text)
    assert (
        output == expected_output
    ), "Failed converting nested bold within italic markdown to HTML"


def test_italic_within_bold():
    input_text = "This is **bold and _italic_ together**."
    expected_output = "This is <b>bold and <i>italic</i> together</b>."
    output = telegram_format(input_text)
    assert (
        output == expected_output
    ), "Failed converting italic within bold markdown to HTML"


def test_inline_code_within_bold_text():
    input_text = "This is **bold and `inline code` together**."
    expected_output = "This is <b>bold and <code>inline code</code> together</b>."
    output = telegram_format(input_text)
    assert output == expected_output, "Failed handling inline code within bold text"


def test_mixed_formatting_tags_with_lists_and_links():
    input_text = """
- This is a list item with **bold**, __underline__, and [a link](http://example.com)
- Another item with ***bold and italic*** text
"""
    expected_output = """
• This is a list item with <b>bold</b>, <u>underline</u>, and <a href="http://example.com">a link</a>
• Another item with <b><i>bold and italic</i></b> text
"""
    output = telegram_format(input_text)
    assert (
        output.strip() == expected_output.strip()
    ), "Failed handling mixed formatting tags with lists and links"


def test_special_characters_within_code_blocks():
    input_text = "Here is a code block: ```<script>alert('Hello')</script>```"
    expected_output = "Here is a code block: <pre><code>&lt;script&gt;alert('Hello')&lt;/script&gt;</code></pre>"
    output = telegram_format(input_text)
    assert (
        output == expected_output
    ), "Failed escaping special characters within code blocks"


def test_code_block_within_bold_text():
    input_text = "This is **bold with a `code block` inside**."
    expected_output = "This is <b>bold with a <code>code block</code> inside</b>."
    output = telegram_format(input_text)
    assert output == expected_output, "Failed handling code block within bold text"


def test_triple_backticks_with_nested_markdown():
    input_text = "```python\n**bold text** and __underline__ in code block```"
    expected_output = '<pre><code class="language-python">**bold text** and __underline__ in code block</code></pre>'
    output = telegram_format(input_text)
    assert (
        output == expected_output
    ), "Failed handling markdown within triple backtick code blocks"


def test_unmatched_code_delimiters():
    input_text = "This has an `unmatched code delimiter."
    expected_output = "This has an <code>unmatched code delimiter.</code>"
    output = telegram_format(input_text)
    assert output == expected_output, "Failed handling unmatched code delimiters"


def test_preformatted_block_with_unusual_language_specification():
    input_text = "```weirdLang\nSome weirdLang code\n```"
    expected_output = (
        '<pre><code class="language-weirdLang">Some weirdLang code\n</code></pre>'
    )
    output = telegram_format(input_text)
    assert (
        output == expected_output
    ), "Failed handling preformatted block with unusual language specification"


def test_inline_code_within_lists():
    input_text = """
- List item with `code`
* Another `code` item
"""
    expected_output = """
• List item with <code>code</code>
• Another <code>code</code> item
"""
    output = telegram_format(input_text)
    assert (
        output.strip() == expected_output.strip()
    ), "Failed handling inline code within lists"


def test_vector_storage_links_trim():
    input_text = """
- List item with `code`
* Another `code` item【4:0†source】
"""
    expected_output = """
• List item with <code>code</code>
• Another <code>code</code> item
"""
    output = telegram_format(input_text)
    assert output.strip() == expected_output.strip(), "Failed trim storage links"


def test_strikethrough_conversion():
    input_text = "This is ~~strikethrough~~ text."
    expected_output = "This is <s>strikethrough</s> text."
    output = telegram_format(input_text)
    assert output == expected_output, "Failed converting ~~ to <s> tags"


def test_blockquote_conversion():
    input_text = "> This is a blockquote."
    expected_output = "<blockquote>This is a blockquote.</blockquote>"
    output = telegram_format(input_text)
    assert output == expected_output, "Failed converting > to <blockquote> tags"


def test_inline_url_conversion():
    input_text = "[example](http://example.com)"
    expected_output = '<a href="http://example.com">example</a>'
    output = telegram_format(input_text)
    assert output == expected_output, "Failed converting [text](URL) to <a> tags"


def test_inline_mention_conversion():
    input_text = "[User](tg://user?id=123456789)"
    expected_output = '<a href="tg://user?id=123456789">User</a>'
    output = telegram_format(input_text)
    assert (
        output == expected_output
    ), "Failed converting [text](tg://user?id=ID) to <a> tags"


def test_escaping_ampersand():
    input_text = "Use & in your HTML."
    expected_output = "Use &amp; in your HTML."
    output = telegram_format(input_text)
    assert output == expected_output, "Failed escaping & character"


def test_pre_and_code_tags_with_html_entities():
    input_text = "```html\n<div>Content</div>\n```"
    expected_output = (
        '<pre><code class="language-html">&lt;div&gt;Content&lt;/div&gt;\n</code></pre>'
    )
    output = telegram_format(input_text)
    assert (
        output == expected_output
    ), "Failed handling pre and code tags with HTML entities"


def test_code_with_multiple_lines():
    input_text = "```\ndef example():\n    return 'example'\n```"
    expected_output = "<pre><code>def example():\n    return 'example'\n</code></pre>"
    output = telegram_format(input_text)
    assert output == expected_output, "Failed handling code with multiple lines"


def test_combined_formatting_with_lists():
    input_text = """
- **Bold** list item
- _Italic_ list item
- `Code` list item
"""
    expected_output = """
• <b>Bold</b> list item
• <i>Italic</i> list item
• <code>Code</code> list item
"""
    output = telegram_format(input_text)
    assert (
        output.strip() == expected_output.strip()
    ), "Failed handling combined formatting with lists"


def test_md_large_example():
    input_text = """
1. **Headings:**
# H1 Heading
## H2 Heading
### H3 Heading
#### H4 Heading
##### H5 Heading
###### H6 Heading

2. **Emphasis:**

*Italic text* or _Italic text_

**Bold text** or __Underline text__

***Bold and italic text*** or ___Underline and italic text___

3. **Lists:**
   - **Unordered List:**

   - Item 1
   - Item 2
     - Subitem 1
     - Subitem 2

   - **Ordered List:**

   1. First item
   2. Second item
      1. Subitem 1
      2. Subitem 2

4. **Links:**

[OpenAI](https://www.openai.com)

5. **Images:**

![Alt text for image](URL_to_image)
![Alt text for image](URL_to_імедж)

6. **Blockquotes:**

> This is a blockquote.
> It can span multiple lines.

7. **Inline Code:**

Here is some `inline code`.

8. **Code Blocks:**

```python
def example_function():
    print("Hello World")
```

9. **Tables:**

| Header 1 | Header 2 |
|----------|----------|
| Row 1 Col 1 | Row 1 Col 2 |
| Row 2 Col 1 | Row 2 Col 2 |

10. **Horizontal Rule:**

---
"""
    expected_output = """
1. <b>Headings:</b>
<b>H1 Heading</b>
<b>H2 Heading</b>
<b>H3 Heading</b>
<b>H4 Heading</b>
<b>H5 Heading</b>
<b>H6 Heading</b>

2. <b>Emphasis:</b>

<i>Italic text</i> or <i>Italic text</i>

<b>Bold text</b> or <u>Underline text</u>

<b><i>Bold and italic text</i></b> or <u><i>Underline and italic text</i></u>

3. <b>Lists:</b>
   • <b>Unordered List:</b>

   • Item 1
   • Item 2
     • Subitem 1
     • Subitem 2

   • <b>Ordered List:</b>

   1. First item
   2. Second item
      1. Subitem 1
      2. Subitem 2

4. <b>Links:</b>

<a href="https://www.openai.com">OpenAI</a>

5. <b>Images:</b>

<a href="URL_to_image">Alt text for image</a>
<a href="URL_to_імедж">Alt text for image</a>

6. <b>Blockquotes:</b>

<blockquote>This is a blockquote.
It can span multiple lines.</blockquote>

7. <b>Inline Code:</b>

Here is some <code>inline code</code>.

8. <b>Code Blocks:</b>

<pre><code class="language-python">def example_function():
    print("Hello World")
</code></pre>

9. <b>Tables:</b>

| Header 1 | Header 2 |
|----------|----------|
| Row 1 Col 1 | Row 1 Col 2 |
| Row 2 Col 1 | Row 2 Col 2 |

10. <b>Horizontal Rule:</b>

---
"""
    output = telegram_format(input_text)
    assert (
        output.strip() == expected_output.strip()
    ), "Failed handling large markdown example"


def test_unclosed_single_backtick():
    """Test that a single unclosed backtick is properly handled"""
    text = "Here is some `code without closing"
    result = ensure_closing_delimiters(text)
    assert result == "Here is some `code without closing`"


def test_unclosed_triple_backtick():
    """Test that unclosed triple backticks are properly handled"""
    text = "Here is some ```code without closing"
    result = ensure_closing_delimiters(text)
    assert result == "Here is some ```code without closing```"


def test_bracket_link_with_additional_text():
    """
    Ensures that text like '[OtherText] [Title](Link)' doesn't
    merge 'OtherText' and 'Title' into the <a> tag text.
    """
    input_text = "[OtherText] [Title](https://example.com)"
    output = telegram_format(input_text)
    expected_output = '[OtherText] <a href="https://example.com">Title</a>'
    assert output == expected_output, f"Output was: {output}"


def test_heading_formatting_with_newlines():
    """
    Checks that headings #, ##, etc. are properly wrapped in <b> tags.
    """
    input_text = """# Heading1
Some text
## Heading2
More text
"""
    output = telegram_format(input_text)
    lines = output.splitlines()

    assert "<b>Heading1</b>" in output
    assert "<b>Heading2</b>" in output
    assert lines[0] == "<b>Heading1</b>"
    assert lines[1] == "Some text"
    assert lines[2] == "<b>Heading2</b>"
    assert lines[3] == "More text"


def test_list_formatting_with_newlines():
    """
    Checks that list items (starting with '-' or '*') become bullet points,
    each on its own line with proper spacing.
    """
    input_text = """- Item one
- Item two
* Item three
Some text
- Item four"""
    output = telegram_format(input_text)
    lines = [line.strip() for line in output.splitlines() if line.strip()]

    assert "• Item one" in lines
    assert "• Item two" in lines
    assert "• Item three" in lines
    assert "• Item four" in lines
    assert "Some text" in lines

    bullet_lines = [line for line in lines if line.startswith("•")]
    assert len(bullet_lines) == 4
    assert bullet_lines[0] == "• Item one"
    assert bullet_lines[1] == "• Item two"
    assert bullet_lines[2] == "• Item three"
    assert bullet_lines[3] == "• Item four"


def test_preserve_other_brackets():
    """
    Ensures that other bracketed text not forming a valid link is preserved literally.
    """
    input_text = "Look at [this], but [not a link] something else."
    output = telegram_format(input_text)
    assert "[this]" in output
    assert "[not a link]" in output
    assert "<a href=" not in output


def test_link_with_nested_brackets():
    """Test that links with nested brackets in the text are handled correctly"""
    input_text = "[Link [with brackets]](https://example.com)"
    output = telegram_format(input_text)
    expected_output = '<a href="https://example.com">Link [with brackets]</a>'
    assert output == expected_output, f"Output was: {output}"


def test_link_with_spaces():
    """Test that links with spaces are handled correctly"""
    input_text = "[OtherText] [Title](Link)"
    output = telegram_format(input_text)
    expected_output = '[OtherText] <a href="Link">Title</a>'
    assert output == expected_output, f"Output was: {output}"


def test_ukrainian_bullet_points():
    input_text = """Звісно, ось список цікавих речей у форматі Markdown:

*  **Парадокс кота Шредінгера:** Чи може кіт бути одночасно живим і мертвим? 🤔
*  **Ефект метелика:** Маленька зміна може мати великі наслідки. 🦋
*  **Теорія струн:** Чи є наш всесвіт просто вібрацією струн? 🎶
*  **Темна матерія та темна енергія:** Що складає 95% всесвіту? 🌌
*  **Квантова заплутаність:** Чи можуть два об'єкти бути зв'язані на відстані? 🔗
*  **Соліпсизм:** Чи існує щось, крім моєї свідомості? 🤨
*  **Парадокс Фермі:** Де всі інші інопланетяни? 👽
*  **Симуляційна гіпотеза:** Чи живемо ми в симуляції? 💻
*  **Ефект Даннінга-Крюгера:** Чому некомпетентні люди переоцінюють себе? 🤓
*  **Когнітивні спотворення:** Як наш мозок обманює нас? 🤯
"""

    expected_output = """Звісно, ось список цікавих речей у форматі Markdown:

• <b>Парадокс кота Шредінгера:</b> Чи може кіт бути одночасно живим і мертвим? 🤔
• <b>Ефект метелика:</b> Маленька зміна може мати великі наслідки. 🦋
• <b>Теорія струн:</b> Чи є наш всесвіт просто вібрацією струн? 🎶
• <b>Темна матерія та темна енергія:</b> Що складає 95% всесвіту? 🌌
• <b>Квантова заплутаність:</b> Чи можуть два об'єкти бути зв'язані на відстані? 🔗
• <b>Соліпсизм:</b> Чи існує щось, крім моєї свідомості? 🤨
• <b>Парадокс Фермі:</b> Де всі інші інопланетяни? 👽
• <b>Симуляційна гіпотеза:</b> Чи живемо ми в симуляції? 💻
• <b>Ефект Даннінга-Крюгера:</b> Чому некомпетентні люди переоцінюють себе? 🤓
• <b>Когнітивні спотворення:</b> Як наш мозок обманює нас? 🤯
"""

    output = telegram_format(input_text)
    print(output)
    assert output.strip() == expected_output.strip()


def test_asterisk_in_equations():
    """Test that asterisks in mathematical equations are not converted to italic"""
    test_cases = [
        ("2 * 2 = 4", "2 * 2 = 4"),
        ("x*y + z = 10", "x*y + z = 10"),
        ("a * b * c", "a * b * c"),
        ("2*x + 3*y = z", "2*x + 3*y = z"),
        ("This is *italic* but 2 * 2 is not", "This is <i>italic</i> but 2 * 2 is not"),
        ("5 * x + *emphasized* text", "5 * x + <i>emphasized</i> text"),
    ]

    for input_text, expected_output in test_cases:
        output = telegram_format(input_text)
        assert (
            output == expected_output
        ), f"Failed on input: {input_text}, got: {output}"


def test_complex_equations_with_asterisk():
    """Test more complex mathematical expressions with asterisks"""
    input_text = """The formula is:
f(x) = 2*x + 3*y
g(x) = x * (y + z)
This is *italic* text with equation 2 * 2 = 4
"""
    expected_output = """The formula is:
f(x) = 2*x + 3*y
g(x) = x * (y + z)
This is <i>italic</i> text with equation 2 * 2 = 4"""

    output = telegram_format(input_text)
    assert output.strip() == expected_output.strip(), f"Output was: {output}"


# ----------------------------------------------------------------------------------------
# New, more comprehensive and edge-case test methods begin here
# ----------------------------------------------------------------------------------------


def test_empty_string():
    """Check behavior with an empty string."""
    input_text = ""
    output = telegram_format(input_text)
    assert output == ""


def test_spaces_only():
    """Check behavior with a string that has only spaces."""
    input_text = "    "
    output = telegram_format(input_text)
    # Should either remain blank or just be those spaces (strip() might remove them)
    assert output.strip() == ""


def test_asterisk_in_parentheses():
    """Edge case with asterisk in parentheses."""
    input_text = "(2*3) is an equation, but *italic* text is separate."
    expected_output = "(2*3) is an equation, but <i>italic</i> text is separate."
    output = telegram_format(input_text)
    assert output == expected_output


def test_underscore_in_non_italic_context():
    """Edge case with underscores that should not convert to italic."""
    input_text = "This_variable should remain, but _italic_ should convert."
    expected_output = "This_variable should remain, but <i>italic</i> should convert."
    output = telegram_format(input_text)
    assert output == expected_output


def test_code_block_mixed_with_unescaped_html():
    """Ensure code block remains escaped but outside text is processed normally."""
    input_text = """
Some <div>stuff</div> here.
```
<html><body>Unescaped?</body></html>
```
More text with *italic*.
"""
    expected_output = """
Some &lt;div&gt;stuff&lt;/div&gt; here.
<pre><code>&lt;html&gt;&lt;body&gt;Unescaped?&lt;/body&gt;&lt;/html&gt;
</code></pre>
More text with <i>italic</i>.
"""
    output = telegram_format(input_text)
    assert output.strip() == expected_output.strip()


def test_equation_with_asterisks_and_italics_combined():
    """More advanced check: combine equations and true italics side by side."""
    input_text = "2*x + 3*y = 10, and *italic* is separate."
    expected_output = "2*x + 3*y = 10, and <i>italic</i> is separate."
    output = telegram_format(input_text)
    assert output == expected_output


def test_inline_code_with_asterisk_and_underscore():
    """Ensure that `*` and `_` inside inline code are not interpreted as markdown."""
    input_text = "Here is `code_with_*_asterisk` outside of `code_with__underscore__`"
    expected_output = "Here is <code>code_with_*_asterisk</code> outside of <code>code_with__underscore__</code>"
    output = telegram_format(input_text)
    assert output == expected_output


def test_heading_followed_by_equation():
    """Check heading usage right before an equation line."""
    input_text = """# MyHeading
2*x + y = 4
"""
    # Heading should become <b>MyHeading</b>, equation line remains as is
    expected_output = """<b>MyHeading</b>
2*x + y = 4"""
    output = telegram_format(input_text)
    assert output.strip() == expected_output.strip(), f"Got: {output}"


def test_spoiler_conversion():
    input_text = "This contains a ||spoiler|| text"
    expected_output = 'This contains a <span class="tg-spoiler">spoiler</span> text'
    output = telegram_format(input_text)
    assert (
        output == expected_output
    ), 'Failed converting || to <span class="tg-spoiler"> tags'


def test_spoiler_with_formatting():
    input_text = "This contains a ||*italic spoiler*|| text"
    expected_output = (
        'This contains a <span class="tg-spoiler"><i>italic spoiler</i></span> text'
    )
    output = telegram_format(input_text)
    assert (
        output == expected_output
    ), "Failed converting nested formatting within spoiler tags"


def test_expandable_blockquote_conversion():
    input_text = """**>The expandable block quotation started
>Expandable block quotation continued
>The last line of the expandable block quotation"""
    expected_output = """<blockquote expandable>The expandable block quotation started
Expandable block quotation continued
The last line of the expandable block quotation</blockquote>"""
    output = telegram_format(input_text)
    assert output == expected_output, "Failed converting expandable blockquote"


def test_regular_and_expandable_blockquotes():
    input_text = """>Regular blockquote
>Regular blockquote continued

**>Expandable blockquote
>Expandable blockquote continued"""
    expected_output = """<blockquote>Regular blockquote
Regular blockquote continued</blockquote>

<blockquote expandable>Expandable blockquote
Expandable blockquote continued</blockquote>"""
    output = telegram_format(input_text)
    assert (
        output.strip() == expected_output.strip()
    ), "Failed handling mixed blockquote types"


def test_blockquote_with_spoiler():
    input_text = """>Regular blockquote with ||spoiler|| text
>Continued"""
    expected_output = """<blockquote>Regular blockquote with <span class="tg-spoiler">spoiler</span> text
Continued</blockquote>"""
    output = telegram_format(input_text)
    assert output == expected_output, "Failed handling spoiler inside blockquote"


def test_multiple_spoilers():
    input_text = "First ||spoiler|| and then another ||spoiler with *italic*||"
    expected_output = 'First <span class="tg-spoiler">spoiler</span> and then another <span class="tg-spoiler">spoiler with <i>italic</i></span>'
    output = telegram_format(input_text)
    assert output == expected_output, "Failed handling multiple spoilers"


def test_ukrainian_text_with_inline_code():
    """Test that Ukrainian text with inline code is properly formatted"""
    input_text = (
        """звісно, майстре тестування. ой та зрозуміло `<LAUGH>` що ти тут тестуєш."""
    )
    expected_output = """звісно, майстре тестування. ой та зрозуміло <code>&lt;LAUGH&gt;</code> що ти тут тестуєш."""
    output = telegram_format(input_text)
    assert output == expected_output, f"Output was: {output}"


def test_nested_code_fence_quadruple():
    input_text = """````markdown
```python
def hello_world():
    print("Hello, World!")
```
````"""
    expected_output = (
        "<pre><code class=\"language-markdown\">```python\n"
        "def hello_world():\n    print(\"Hello, World!\")\n```\n</code></pre>"
    )
    output = telegram_format(input_text)
    def show_output():
      print(f"Expected was: \n\n{expected_output}\n\n")
      print(f"output was: \n\n{output}")
    assert output == expected_output, show_output()


def test_nested_code_fence_quadruple_no_lang():
    input_text = """````
```python
print('hi')
```
````"""
    expected_output = (
        "<pre><code>```python\nprint('hi')\n```\n</code></pre>"
    )
    output = telegram_format(input_text)
    def show_output():
      print(f"Expected was: \n\n{expected_output}\n\n")
      print(f"output was: \n\n{output}")
    assert output == expected_output, show_output()


def test_nested_code_fence_five_backticks():
    input_text = """`````markdown
````python
print(1)
````
`````"""
    expected_output = (
        "<pre><code class=\"language-markdown\">````python\nprint(1)\n````\n</code></pre>"
    )
    output = telegram_format(input_text)
    def show_output():
      print(f"Expected was: \n\n{expected_output}\n\n")
      print(f"output was: \n\n{output}")
    assert output == expected_output, show_output()


def test_nested_code_fence_five_backticks_with_inner_triple():
    input_text = """`````markdown
````python
print("hello world ```")
````
`````"""
    expected_output = (
        "<pre><code class=\"language-markdown\">````python\n"
        "print(\"hello world ```\")\n````\n</code></pre>"
    )
    output = telegram_format(input_text)
    def show_output():
      print(f"Expected was: \n\n{expected_output}\n\n")
      print(f"output was: \n\n{output}")
    assert output == expected_output, show_output()


def test_nested_code_fence_six_backticks():
    input_text = """``````markdown
`````python
print('hi')
`````
``````"""
    expected_output = """<pre><code class=\"language-markdown\">`````python
print('hi')
`````
</code></pre>"""
    output = telegram_format(input_text)
    def show_output():
      print(f"Expected was: \n\n{expected_output}\n\n")
      print(f"output was: \n\n{output}")
    assert output == expected_output, show_output()


def test_nested_code_fence_plain_text():
    input_text = """
````markdown
```
hello
```
````"""
    expected_output = """<pre><code class=\"language-markdown\">```
hello
```
</code></pre>"""
    output = telegram_format(input_text)
    def show_output():
      print(f"Expected was: \n\n{expected_output}\n\n")
      print(f"output was: \n\n{output}")
    assert output == expected_output, show_output()





def test_expensive_nested_code_five_fence_plain_text():
    input_text = """
`````markdown
````
```python
print("hello world ```")
```
`````"""

    expected_output = """<pre><code class=\"language-markdown\">````
```python
print("hello world ```")
```
</code></pre>"""
    output = telegram_format(input_text)
    def show_output():
      print(f"Expected was: \n\n{expected_output}\n\n")
      print(f"output was: \n\n{output}")
    assert output == expected_output, show_output()

def test_another_expensive_nested_code_five_fence_plain_text():
    input_text = """`````markdown
````python
print("hello world ```"')
```
`````"""

    expected_output = """<pre><code class=\"language-markdown\">````python
print("hello world ```"')
```
</code></pre>"""
    output = telegram_format(input_text)
    def show_output():
      print(f"Expected was: \n\n{expected_output}\n\n")
      print(f"output was: \n\n{output}")
    assert output == expected_output, show_output()

def test_hard_level_nested_code_five_fence_plain_text():
    input_text = """`````markdown
````python
print("hello world ```"')
````
`````
```python
print("Some another text")""" # That's where closing the second block of python code is missing.

    expected_output = """<pre><code class="language-markdown">````python
print("hello world ```"')
````
</code></pre>
<pre><code class="language-python">print("Some another text")
</code></pre>""" # But the code block is still closed correctly.
    
    output = telegram_format(input_text)
    def show_output():
      print(f"Expected was: \n\n{expected_output}\n\n")
      print(f"output was: \n\n{output}")
    assert output == expected_output, show_output()

def test_hard_level_nested_code_five_fence_plain_text_2():
    input_text = """`````markdown
````python
print("hello world ```"')
`````
```python
print("Some another text")""" # That's where closing the second block of python code is missing.

    expected_output = """<pre><code class="language-markdown">````python
print("hello world ```"')
</code></pre>
<pre><code class="language-python">print("Some another text")
</code></pre>""" # But the code block is still closed correctly.
    
    output = telegram_format(input_text)
    def show_output():
      print(f"Expected was: \n\n{expected_output}\n\n")
      print(f"output was: \n\n{output}")
    assert output == expected_output, show_output()

def test_some_new():
    input_text = """
``````markdown
`````
````python
print("hello world ```")
```
""" # Markdown code wasn't closed

    expected_output = """<pre><code class=\"language-markdown\">`````
````python
print("hello world ```")
```
</code></pre>""" # But after closed correctly
    output = telegram_format(input_text)
    def show_output():
      print(f"Expected was: \n\n{expected_output}\n\n")
      print(f"output was: \n\n{output}")
    assert output == expected_output, show_output()