import json
import pandas as pd
import re

# Load synonym list from JSON file
with open('synonyms.json', 'r') as f:
    synonym_lines = json.load(f)

# Build synonym map (all lowercase for case-insensitive matching)
synonym_map = {}
for line in synonym_lines:
    parts = [p.strip() for p in line.split(',')]
    full_form = parts[1].capitalize() if len(parts) > 1 else parts[0]
    for synonym in parts:
        synonym_map[synonym.strip().lower()] = full_form

# Compile a regex pattern that matches any synonym
synonym_pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in sorted(synonym_map, key=len, reverse=True)) + r')\b', re.IGNORECASE)

# Function to replace synonyms in a single string
def replace_synonyms_in_text(text):
    return synonym_pattern.sub(lambda m: synonym_map.get(m.group(0).lower(), m.group(0)), text)

# Function to process the list of strings (split_rules)
def replace_synonyms_in_list(rule_list):
    return [replace_synonyms_in_text(rule) for rule in rule_list]

# Sample DataFrame
data = {
    "id": [1, 2],
    "name": ["example1", "example2"],
    "type": ["A", "B"],
    "split_rules": [
        ["1: CY for this year will be high"],
        ["GWM performance has grown"]
    ]
}
df = pd.DataFrame(data)

# Apply the replacement function to the split_rules column
df['split_rules'] = df['split_rules'].apply(replace_synonyms_in_list)

# Show result
print(df)
