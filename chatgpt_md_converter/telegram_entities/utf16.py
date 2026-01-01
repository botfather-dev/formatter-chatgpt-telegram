"""UTF-16 encoding utilities for Telegram entity offset calculation."""


def utf16_len(text: str) -> int:
    """
    Calculate the length of a string in UTF-16 code units.

    Telegram uses UTF-16 code units for entity offsets and lengths.
    Characters outside the Basic Multilingual Plane (like emoji) take 2 units.

    Args:
        text: The string to measure

    Returns:
        Length in UTF-16 code units
    """
    return len(text.encode("utf-16-le")) // 2


def char_to_utf16_offset(text: str, char_index: int) -> int:
    """
    Convert a Python string index to a UTF-16 offset.

    Args:
        text: The full text string
        char_index: Python string index (0-based)

    Returns:
        UTF-16 offset for the same position
    """
    return utf16_len(text[:char_index])


def utf16_to_char_offset(text: str, utf16_offset: int) -> int:
    """
    Convert a UTF-16 offset to a Python string index.

    Args:
        text: The full text string
        utf16_offset: UTF-16 offset

    Returns:
        Python string index for the same position
    """
    current_utf16 = 0
    for i, char in enumerate(text):
        if current_utf16 >= utf16_offset:
            return i
        current_utf16 += len(char.encode("utf-16-le")) // 2
    return len(text)
