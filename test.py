import re

def clean_invisible_chars(text):
    """
    Removes all invisible, zero-width, and non-printable characters from the input string.
    Keeps normal letters, numbers, punctuation, and spaces.
    """
    # Regex for:
    # - Zero-width chars: ZWSP, ZWNJ, ZWJ, Word Joiner, BOM
    # - ASCII control chars: \x00-\x1F, \x7F
    invisible_pattern = r'[\u200B\u200C\u200D\u2060\uFEFF\x00-\x1F\x7F]'
    
    # Substitute them with empty string
    return re.sub(invisible_pattern, '', text)


# Example
s = "H\u200Bello\u200C \u200DWo\u2060rld!\n\t"
clean_s = clean_invisible_chars(s)

print(clean_s)
