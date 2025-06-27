from langchain_openai import AzureChatOpenAI
import pandas as pd
import json

# Load synonyms from JSON file
with open('synonyms.json', 'r', encoding='utf-8') as f:
    synonym_lines = json.load(f)

# Convert list of synonym lines into a structured dictionary
def build_synonym_dict(synonym_lines):
    synonym_dict = {}
    for line in synonym_lines:
        if "=>" in line:
            parts = [p.strip() for p in line.split("=>")]
            if len(parts) == 2:
                synonym_dict[parts[0]] = parts[1]
        elif "," in line:
            parts = [p.strip() for p in line.split(",")]
            full_form = parts[1] if len(parts) > 1 else parts[0]
            for synonym in parts:
                synonym_dict[synonym] = full_form
    return synonym_dict

synonym_dict = build_synonym_dict(synonym_lines)

# Initialize LLM
llm = AzureChatOpenAI(
    api_key="<your-azure-api-key>",
    azure_endpoint="<your-azure-endpoint>",
    api_version="2023-05-15",
    deployment_name="gpt-4",
    temperature=0.3
)

# Function to rewrite a list of rules using LLM
def rewrite_rules_with_llm(rule_list):
    rules_text = "\n".join(f"- {rule}" for rule in rule_list)
    synonyms_json = json.dumps(synonym_dict, indent=2)

    user_prompt = f"""You are a structured assistant that rewrites business rules using a synonym mapping.

Your task is to:
1. First replace terms in the rules using the following synonym dictionary:
{synonyms_json}

2. Then rewrite the rules into clear, atomic English instructions.
   - Break down compound sentences.
   - Make all time comparisons explicit based on the first line.
   - Use hierarchical sub-point numbering like 1.1, 1.2, etc.
   - Keep abbreviations like NPBT, DCM, GWM exactly as-is (case-sensitive).
   - Avoid repeating phrases like "the same" — rewrite those explicitly.

Here are the rules to rewrite:
{rules_text}
"""

    response = llm.invoke([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_prompt}
    ])

    output_lines = response.content.split("\n")
    return [line.strip("-• ").strip() for line in output_lines if line.strip()]

# Example usage
df = pd.DataFrame({
    "split_rules": [
        ["CY for this year will be high", "Income is growing"],
        ["GWM performance has grown", "Resources are insufficient this quarter"]
    ]
})

# Apply
df['rephrased_rules'] = df['split_rules'].apply(rewrite_rules_with_llm)
print(df[['split_rules', 'rephrased_rules']])
