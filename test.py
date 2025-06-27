import json
import pandas as pd
import re

# Load synonym list from JSON file
with open('synonyms.json', 'r', encoding='utf-8') as f:
    synonym_lines = json.load(f)

# Build synonym map (case-insensitive)
synonym_map = {}
for line in synonym_lines:
    # Handle "=>" format
    if "=>" in line:
        parts = [p.strip() for p in line.split("=>")]
        if len(parts) == 2:
            synonym_map[parts[0].lower()] = parts[1]
    # Handle comma-separated format
    elif "," in line:
        parts = [p.strip() for p in line.split(",")]
        full_form = parts[1].capitalize() if len(parts) > 1 else parts[0]
        for synonym in parts:
            synonym_map[synonym.lower()] = full_form

# Compile a regex pattern for all synonyms (longer first to avoid partial matches)
synonym_pattern = re.compile(
    r'\b(' + '|'.join(re.escape(k) for k in sorted(synonym_map, key=len, reverse=True)) + r')\b',
    re.IGNORECASE
)

# Replace synonyms in a single string
def replace_synonyms_in_text(text):
    return synonym_pattern.sub(lambda m: synonym_map.get(m.group(0).lower(), m.group(0)), text)

# Replace synonyms in list of strings
def replace_synonyms_in_list(rule_list):
    return [replace_synonyms_in_text(rule) for rule in rule_list]

# Sample DataFrame
data = {
    "id": [1, 2],
    "name": ["example1", "example2"],
    "type": ["A", "B"],
    "split_rules": [
        ["1: CY for this year will be high", "Income is growing"],
        ["GWM performance has grown", "Mom variance is seen"]
    ]
}
df = pd.DataFrame(data)

# Apply synonym replacement
df['split_rules'] = df['split_rules'].apply(replace_synonyms_in_list)

# Print result
print(df[['id', 'split_rules']])
