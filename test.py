import re

s = "Hello\u200BWorld\u200C\u200D\uFEFF!\n\t"

# Regex to match:
# - Zero-width characters: ZWSP, ZWNJ, ZWJ, BOM
# - Other non-printable/control characters: \x00-\x1F, \x7F
invisible_pattern = r'[\u200B\u200C\u200D\uFEFF\x00-\x1F\x7F]'

s_clean = re.sub(invisible_pattern, '', s)

print(s_clean)
