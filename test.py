import json
import pandas as pd
import re

# Simulated synonym lines
synonym_lines = [
    "Mom, month over month",
    "Income => Net Income",
    "CY, current year",
    "GWM, Global Wealth Management"
]

# Build synonym map
synonym_map = {}
for line in synonym_lines:
    if "=>" in line:
        parts = [p.strip() for p in line.split("=>")]
        if len(parts) == 2:
            synonym_map[parts[0].lower()] = parts[1]
    elif "," in line:
        parts = [p.strip() for p in line.split(",")]
        full_form = parts[1].capitalize() if len(parts) > 1 else parts[0]
        for synonym in parts:
            synonym_map[synonym.lower()] = full_form

# Pattern
synonym_pattern = re.compile(
    r'\b(' + '|'.join(re.escape(k) for k in sorted(synonym_map, key=len, reverse=True)) + r')\b',
    re.IGNORECASE
)

# Replacers
def replace_synonyms_in_text(text):
    return synonym_pattern.sub(lambda m: synonym_map.get(m.group(0).lower(), m.group(0)), text)

def replace_synonyms_in_list(rule_list):
    if isinstance(rule_list, str):
        rule_list = [rule_list]
    return [replace_synonyms_in_text(rule) for rule in rule_list]

# Sample DataFrame
data = {
    "id": [1, 2],
    "split_rules": [
        ["CY for this year will be high", "Income is growing"],
        "GWM performance has grown"  # ← single string
    ]
}
df = pd.DataFrame(data)

# Apply fix
df['split_rules'] = df['split_rules'].apply(replace_synonyms_in_list)

# Result
print(df[['id', 'split_rules']])
