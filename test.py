import json

try:
    # Try to parse JSON output from the LLM
    summary_dict = json.loads(text)
except json.JSONDecodeError as e:
    # Optionally try to clean up common formatting issues
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    try:
        summary_dict = json.loads(cleaned)
    except Exception as e2:
        raise ValueError(f"Failed to parse LLM output: {text[:300]}...\nError: {e2}")

batch_summaries = []
for row_id in comment_dict.keys():
    original = row_mapping.get(row_id)
    summary = summary_dict.get(row_id, {})  # safer with default
