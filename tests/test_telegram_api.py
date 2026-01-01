"""
Tests that verify entity conversion against real Telegram API.

These tests require:
1. aiogram installed: pip install aiogram
2. A Telegram bot token in .env file (TELEGRAM_BOT_TOKEN)
3. A chat ID where the bot can send messages (TELEGRAM_CHAT_ID)

Run with: python -m pytest tests/test_telegram_api.py -v -s

The tests send messages using our generated entities and verify
they are accepted by Telegram.
"""

import os
from typing import Any, Dict, List, Optional, Tuple

import pytest

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Try to import aiogram
try:
    from aiogram import Bot
    from aiogram.enums import MessageEntityType
    from aiogram.types import MessageEntity
    HAS_AIOGRAM = True
except ImportError:
    HAS_AIOGRAM = False
    Bot = None
    MessageEntity = None
    MessageEntityType = None

from chatgpt_md_converter import telegram_format_entities

# Get credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Determine if tests should be skipped
SKIP_REASON = None
if not HAS_AIOGRAM:
    SKIP_REASON = "aiogram not installed. Run: pip install aiogram"
elif not TELEGRAM_BOT_TOKEN:
    SKIP_REASON = "TELEGRAM_BOT_TOKEN not set in environment"
elif not TELEGRAM_CHAT_ID:
    SKIP_REASON = "TELEGRAM_CHAT_ID not set in environment"

pytestmark = pytest.mark.skipif(
    SKIP_REASON is not None,
    reason=SKIP_REASON or "Telegram not configured"
)


@pytest.fixture
def bot():
    """Create a bot instance."""
    if not HAS_AIOGRAM or not TELEGRAM_BOT_TOKEN:
        pytest.skip("Telegram not configured")
    return Bot(token=TELEGRAM_BOT_TOKEN)


@pytest.fixture
def chat_id():
    """Get the chat ID."""
    if not TELEGRAM_CHAT_ID:
        pytest.skip("TELEGRAM_CHAT_ID not set")
    return int(TELEGRAM_CHAT_ID)


def entity_to_dict(entity: "MessageEntity") -> Dict[str, Any]:
    """Convert a MessageEntity to a comparable dict."""
    result = {
        "type": entity.type.value if hasattr(entity.type, 'value') else str(entity.type),
        "offset": entity.offset,
        "length": entity.length,
    }
    if entity.url:
        result["url"] = entity.url
    if entity.language:
        result["language"] = entity.language
    return result


def normalize_url(url: Optional[str]) -> Optional[str]:
    """Normalize URL for comparison (remove trailing slash)."""
    if url is None:
        return None
    return url.rstrip("/")


def compare_entities(
    our_entities: List[Dict[str, Any]],
    telegram_entities: List["MessageEntity"],
) -> Tuple[bool, str]:
    """
    Compare our entities with Telegram's entities.
    Returns (match, diff_description)
    """
    if telegram_entities is None:
        telegram_entities = []

    tg_dicts = [entity_to_dict(e) for e in telegram_entities]

    # Normalize URLs in both lists
    our_copy = [dict(e) for e in our_entities]
    for e in our_copy:
        if "url" in e:
            e["url"] = normalize_url(e["url"])
    for e in tg_dicts:
        if "url" in e:
            e["url"] = normalize_url(e["url"])

    # Sort both by offset, then by length
    our_sorted = sorted(our_copy, key=lambda e: (e["offset"], e["length"]))
    tg_sorted = sorted(tg_dicts, key=lambda e: (e["offset"], e["length"]))

    if our_sorted == tg_sorted:
        return True, "Match!"

    diff = f"Our entities: {our_sorted}\nTelegram entities: {tg_sorted}"
    return False, diff


def our_entities_to_aiogram(entities: List[Dict[str, Any]]) -> List["MessageEntity"]:
    """Convert our entity dicts to aiogram MessageEntity objects."""
    result = []
    for e in entities:
        entity_type = e["type"]
        # Map string type to MessageEntityType enum
        type_map = {
            "bold": MessageEntityType.BOLD,
            "italic": MessageEntityType.ITALIC,
            "underline": MessageEntityType.UNDERLINE,
            "strikethrough": MessageEntityType.STRIKETHROUGH,
            "spoiler": MessageEntityType.SPOILER,
            "code": MessageEntityType.CODE,
            "pre": MessageEntityType.PRE,
            "text_link": MessageEntityType.TEXT_LINK,
            "blockquote": MessageEntityType.BLOCKQUOTE,
            "expandable_blockquote": MessageEntityType.EXPANDABLE_BLOCKQUOTE,
        }

        msg_entity = MessageEntity(
            type=type_map.get(entity_type, entity_type),
            offset=e["offset"],
            length=e["length"],
            url=e.get("url"),
            language=e.get("language"),
        )
        result.append(msg_entity)
    return result


class TestTelegramMarkdownV2Comparison:
    """
    Test that our entity generation works with Telegram API.

    These tests send content using our generated entities and verify
    the message is accepted by Telegram.
    """

    @pytest.mark.asyncio
    async def test_bold_text(self, bot, chat_id):
        """Test bold text conversion."""
        markdown = "**Hello bold world**"

        text, our_entities = telegram_format_entities(markdown)
        print(f"\nInput: {markdown}")
        print(f"Our text: {text}")
        print(f"Our entities: {our_entities}")

        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        print(f"Telegram entities: {[entity_to_dict(e) for e in msg.entities or []]}")

        match, diff = compare_entities(our_entities, msg.entities or [])
        assert match, f"Entity mismatch:\n{diff}"

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()

    @pytest.mark.asyncio
    async def test_italic_text(self, bot, chat_id):
        """Test italic text conversion."""
        markdown = "*Hello italic world*"

        text, our_entities = telegram_format_entities(markdown)
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        match, diff = compare_entities(our_entities, msg.entities or [])
        assert match, f"Entity mismatch:\n{diff}"

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()

    @pytest.mark.asyncio
    async def test_code_text(self, bot, chat_id):
        """Test inline code conversion."""
        markdown = "Use `print('hello')` for output"

        text, our_entities = telegram_format_entities(markdown)
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        match, diff = compare_entities(our_entities, msg.entities or [])
        assert match, f"Entity mismatch:\n{diff}"

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()

    @pytest.mark.asyncio
    async def test_link(self, bot, chat_id):
        """Test link conversion."""
        markdown = "Check out [Google](https://google.com)"

        text, our_entities = telegram_format_entities(markdown)
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        match, diff = compare_entities(our_entities, msg.entities or [])
        assert match, f"Entity mismatch:\n{diff}"

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()

    @pytest.mark.asyncio
    async def test_multiple_formats(self, bot, chat_id):
        """Test multiple formatting types."""
        markdown = "**bold** and *italic* and `code`"

        text, our_entities = telegram_format_entities(markdown)
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        match, diff = compare_entities(our_entities, msg.entities or [])
        assert match, f"Entity mismatch:\n{diff}"

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()

    @pytest.mark.asyncio
    async def test_nested_formatting(self, bot, chat_id):
        """Test nested formatting (bold with italic inside)."""
        markdown = "**bold with *italic* inside**"

        text, our_entities = telegram_format_entities(markdown)

        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        # Verify we have bold and italic entities
        our_types = {e["type"] for e in our_entities}
        assert "bold" in our_types
        assert "italic" in our_types

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()

    @pytest.mark.asyncio
    async def test_emoji_with_formatting(self, bot, chat_id):
        """Test formatting with emoji (UTF-16 offset test)."""
        markdown = "Hello 😀 **world**"

        text, our_entities = telegram_format_entities(markdown)
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        match, diff = compare_entities(our_entities, msg.entities or [])
        assert match, f"Entity mismatch:\n{diff}"

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()

    @pytest.mark.asyncio
    async def test_code_block(self, bot, chat_id):
        """Test code block conversion."""
        markdown = """```python
def hello():
    print("world")
```"""

        text, our_entities = telegram_format_entities(markdown)
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        match, diff = compare_entities(our_entities, msg.entities or [])
        assert match, f"Entity mismatch:\n{diff}"

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()

    @pytest.mark.asyncio
    async def test_strikethrough(self, bot, chat_id):
        """Test strikethrough conversion."""
        markdown = "This is ~~deleted~~ text"

        text, our_entities = telegram_format_entities(markdown)
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        match, diff = compare_entities(our_entities, msg.entities or [])
        assert match, f"Entity mismatch:\n{diff}"

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()

    @pytest.mark.asyncio
    async def test_spoiler(self, bot, chat_id):
        """Test spoiler conversion."""
        markdown = "Click to reveal: ||secret message||"

        text, our_entities = telegram_format_entities(markdown)
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        match, diff = compare_entities(our_entities, msg.entities or [])
        assert match, f"Entity mismatch:\n{diff}"

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()

    @pytest.mark.asyncio
    async def test_underline(self, bot, chat_id):
        """Test underline conversion."""
        markdown = "This is __underlined__ text"

        text, our_entities = telegram_format_entities(markdown)
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        match, diff = compare_entities(our_entities, msg.entities or [])
        assert match, f"Entity mismatch:\n{diff}"

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()


class TestComplexExamples:
    """Test more complex real-world examples."""

    @pytest.mark.asyncio
    async def test_chatgpt_style_response(self, bot, chat_id):
        """Test a typical ChatGPT-style formatted response."""
        markdown = """# How to use Python

Here's a quick guide:

**Step 1**: Install Python from [python.org](https://python.org)

**Step 2**: Write your first program:

```python
print("Hello, World!")
```

*Pro tip*: Use `pip` to install packages.

~~Old method~~ - Don't use this anymore!
"""

        text, our_entities = telegram_format_entities(markdown)

        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        # Verify all expected entity types are present
        our_types = {e["type"] for e in our_entities}
        expected_types = {"bold", "text_link", "pre", "italic", "code", "strikethrough"}
        assert expected_types.issubset(our_types), f"Missing types: {expected_types - our_types}"

        assert msg.message_id is not None

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()

    @pytest.mark.asyncio
    async def test_multiple_emoji_formatting(self, bot, chat_id):
        """Test with multiple emoji and formatting."""
        markdown = "🎉 **Party time!** 🎊 Let's *celebrate* 🥳"

        text, our_entities = telegram_format_entities(markdown)
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        match, diff = compare_entities(our_entities, msg.entities or [])
        assert match, f"Entity mismatch:\n{diff}"

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()

    @pytest.mark.asyncio
    async def test_all_formats_combined(self, bot, chat_id):
        """Test all formatting types in one message."""
        markdown = """**Bold** *Italic* __Underline__ ~~Strike~~ ||Spoiler||
`inline code` and [link](https://example.com)

```
code block
```"""

        text, our_entities = telegram_format_entities(markdown)

        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            entities=our_entities_to_aiogram(our_entities)
        )

        # Verify all expected entity types are present
        our_types = {e["type"] for e in our_entities}
        expected_types = {"bold", "italic", "underline", "strikethrough", "spoiler", "code", "text_link", "pre"}
        assert expected_types.issubset(our_types), f"Missing types: {expected_types - our_types}"

        assert msg.message_id is not None

        await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
        await bot.session.close()


if __name__ == "__main__":
    import asyncio

    async def quick_test():
        if not HAS_AIOGRAM:
            print("aiogram not installed. Run: pip install aiogram")
            return
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env file")
            return

        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        chat_id = int(TELEGRAM_CHAT_ID)

        markdown = "**Hello** *world* with `code` and 😀 emoji!"
        text, entities = telegram_format_entities(markdown)

        print(f"Input: {markdown}")
        print(f"Output text: {text}")
        print(f"Entities: {entities}")

        try:
            msg = await bot.send_message(
                chat_id=chat_id,
                text=text,
                entities=our_entities_to_aiogram(entities)
            )
            print(f"Message sent! ID: {msg.message_id}")
            print(f"Telegram entities: {[entity_to_dict(e) for e in msg.entities or []]}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await bot.session.close()

    asyncio.run(quick_test())
