"""Tests for Telegram entity conversion."""

from chatgpt_md_converter import telegram_format_entities
from chatgpt_md_converter.telegram_entities.utf16 import utf16_len


def test_bold_entity():
    """Test bold text conversion to entity."""
    text, entities = telegram_format_entities("**bold** text")
    assert text == "bold text"
    assert len(entities) == 1
    assert entities[0]["type"] == "bold"
    assert entities[0]["offset"] == 0
    assert entities[0]["length"] == 4


def test_italic_entity_underscore():
    """Test italic text with underscores."""
    text, entities = telegram_format_entities("_italic_ text")
    assert text == "italic text"
    assert len(entities) == 1
    assert entities[0]["type"] == "italic"
    assert entities[0]["offset"] == 0
    assert entities[0]["length"] == 6


def test_italic_entity_asterisk():
    """Test italic text with asterisks."""
    text, entities = telegram_format_entities("*italic* text")
    assert text == "italic text"
    assert len(entities) == 1
    assert entities[0]["type"] == "italic"
    assert entities[0]["offset"] == 0
    assert entities[0]["length"] == 6


def test_underline_entity():
    """Test underline text conversion."""
    text, entities = telegram_format_entities("__underline__ text")
    assert text == "underline text"
    assert len(entities) == 1
    assert entities[0]["type"] == "underline"
    assert entities[0]["offset"] == 0
    assert entities[0]["length"] == 9


def test_strikethrough_entity():
    """Test strikethrough text conversion."""
    text, entities = telegram_format_entities("~~strikethrough~~ text")
    assert text == "strikethrough text"
    assert len(entities) == 1
    assert entities[0]["type"] == "strikethrough"
    assert entities[0]["offset"] == 0
    assert entities[0]["length"] == 13


def test_spoiler_entity():
    """Test spoiler text conversion."""
    text, entities = telegram_format_entities("||spoiler|| text")
    assert text == "spoiler text"
    assert len(entities) == 1
    assert entities[0]["type"] == "spoiler"
    assert entities[0]["offset"] == 0
    assert entities[0]["length"] == 7


def test_inline_code_entity():
    """Test inline code conversion."""
    text, entities = telegram_format_entities("`code` text")
    assert text == "code text"
    assert len(entities) == 1
    assert entities[0]["type"] == "code"
    assert entities[0]["offset"] == 0
    assert entities[0]["length"] == 4


def test_code_block_entity():
    """Test code block conversion."""
    text, entities = telegram_format_entities("```python\nprint('hello')\n```")
    assert "print('hello')" in text
    assert len(entities) == 1
    assert entities[0]["type"] == "pre"
    assert entities[0]["language"] == "python"


def test_code_block_no_language():
    """Test code block without language specification."""
    text, entities = telegram_format_entities("```\ncode here\n```")
    assert "code here" in text
    assert len(entities) == 1
    assert entities[0]["type"] == "pre"
    assert entities[0].get("language") is None


def test_link_entity():
    """Test link conversion to text_link entity."""
    text, entities = telegram_format_entities("[click here](https://example.com)")
    assert text == "click here"
    assert len(entities) == 1
    assert entities[0]["type"] == "text_link"
    assert entities[0]["offset"] == 0
    assert entities[0]["length"] == 10
    assert entities[0]["url"] == "https://example.com"


def test_heading_to_bold():
    """Test heading conversion to bold entity."""
    text, entities = telegram_format_entities("# Heading")
    assert text == "Heading"
    assert len(entities) == 1
    assert entities[0]["type"] == "bold"
    assert entities[0]["offset"] == 0
    assert entities[0]["length"] == 7


def test_multiple_entities():
    """Test multiple formatting in one text."""
    text, entities = telegram_format_entities("**bold** and *italic*")
    assert text == "bold and italic"
    assert len(entities) == 2

    # Find bold and italic entities
    bold = next(e for e in entities if e["type"] == "bold")
    italic = next(e for e in entities if e["type"] == "italic")

    assert bold["offset"] == 0
    assert bold["length"] == 4
    assert italic["offset"] == 9
    assert italic["length"] == 6


def test_nested_formatting():
    """Test nested formatting (bold with italic inside)."""
    text, entities = telegram_format_entities("**bold *italic* text**")
    assert text == "bold italic text"

    # Should have both bold and italic entities
    types = {e["type"] for e in entities}
    assert "bold" in types
    assert "italic" in types


def test_utf16_offset_with_emoji():
    """Test that offsets are correctly calculated in UTF-16 for emoji."""
    text, entities = telegram_format_entities("Hello 😀 **world**")
    assert text == "Hello 😀 world"

    # Find the bold entity
    bold = next(e for e in entities if e["type"] == "bold")

    # In UTF-16:
    # "Hello " = 6 units
    # "😀" = 2 units (surrogate pair)
    # " " = 1 unit
    # So "world" starts at offset 9
    assert bold["offset"] == 9
    assert bold["length"] == 5


def test_utf16_offset_multiple_emoji():
    """Test UTF-16 offsets with multiple emoji."""
    text, entities = telegram_format_entities("🎉🎊 **party**")
    assert text == "🎉🎊 party"

    bold = next(e for e in entities if e["type"] == "bold")

    # "🎉" = 2 units, "🎊" = 2 units, " " = 1 unit
    # So "party" starts at offset 5
    assert bold["offset"] == 5
    assert bold["length"] == 5


def test_utf16_len_helper():
    """Test the UTF-16 length helper function."""
    assert utf16_len("hello") == 5
    assert utf16_len("😀") == 2
    assert utf16_len("Hello 😀") == 8
    assert utf16_len("🎉🎊") == 4


def test_list_conversion():
    """Test list marker conversion."""
    text, entities = telegram_format_entities("- item 1\n* item 2")
    assert "• item 1" in text
    assert "• item 2" in text


def test_citation_removal():
    """Test ChatGPT citation marker removal."""
    text, entities = telegram_format_entities("Some text【1】 with citation")
    assert "【" not in text
    assert "】" not in text


def test_combined_formatting():
    """Test combined text with multiple formatting types."""
    markdown = """# Title
This is **bold** and *italic*.
Check out [this link](https://example.com).

`inline code` and:

```python
print("hello")
```
"""
    text, entities = telegram_format_entities(markdown)

    # Should have entities for: heading (bold), bold, italic, link, code, pre
    types = {e["type"] for e in entities}

    assert "bold" in types
    assert "italic" in types
    assert "text_link" in types
    assert "code" in types
    assert "pre" in types


def test_empty_text():
    """Test empty text handling."""
    text, entities = telegram_format_entities("")
    assert text == ""
    assert entities == []


def test_plain_text():
    """Test plain text without any formatting."""
    text, entities = telegram_format_entities("Just plain text")
    assert text == "Just plain text"
    assert entities == []


def test_bold_italic_combined():
    """Test ***bold and italic*** syntax."""
    text, entities = telegram_format_entities("***bold italic***")
    assert text == "bold italic"

    types = {e["type"] for e in entities}
    assert "bold" in types
    assert "italic" in types


def test_entity_dict_format():
    """Test that entity dicts have correct format for Telegram API."""
    text, entities = telegram_format_entities("**bold**")

    entity = entities[0]
    assert "type" in entity
    assert "offset" in entity
    assert "length" in entity
    assert isinstance(entity["type"], str)
    assert isinstance(entity["offset"], int)
    assert isinstance(entity["length"], int)


def test_link_with_url_field():
    """Test that link entities have the url field."""
    text, entities = telegram_format_entities("[text](https://example.com)")

    entity = entities[0]
    assert entity["type"] == "text_link"
    assert "url" in entity
    assert entity["url"] == "https://example.com"


def test_code_block_with_language_field():
    """Test that code block entities have the language field."""
    text, entities = telegram_format_entities("```python\ncode\n```")

    entity = entities[0]
    assert entity["type"] == "pre"
    assert "language" in entity
    assert entity["language"] == "python"


def test_special_chars_in_text():
    """Test that special characters are preserved in plain text."""
    text, entities = telegram_format_entities("**bold with < > & chars**")
    assert "< > &" in text


def test_multiple_lines():
    """Test multiline text handling."""
    text, entities = telegram_format_entities("**line 1**\n\n**line 2**")
    assert "line 1" in text
    assert "line 2" in text
    assert len(entities) == 2


def test_escaped_markers():
    """Test that escaped markers are not converted."""
    # Backslash-escaped markers should remain as-is
    text, entities = telegram_format_entities(r"\*\*not bold\*\*")
    # The escaped asterisks should not create a bold entity
    # (depending on implementation, the backslashes may or may not be stripped)
    bold_entities = [e for e in entities if e["type"] == "bold"]
    # Should have no bold entities for escaped markers
    assert len(bold_entities) == 0 or "not bold" not in text[:10]
