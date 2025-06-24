import openai
import pandas as pd

openai.api_type = "azure"
openai.api_base = "https://<your-endpoint>.openai.azure.com/"
openai.api_key = "<your-api-key>"
openai.api_version = "2023-05-15"

deployment_name = "gpt-4"  # your deployed model name

def call_azure_gpt(rules_list):
    rules_text = "\n".join([f"- {r}" for r in rules_list])
    prompt = f"""
You are an assistant helping to rephrase and decompose business logic rules into clear English. 
Rewrite each of the following rules as a clean, natural sentence:

{rules_text}
"""

    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=500
    )

    return response.choices[0].message['content'].split("\n")

# Apply to dataframe
def gpt_rephrase_row(rule_list):
    output_lines = call_azure_gpt(rule_list)
    # Clean and keep only rephrased lines (ignore empty or numbering if any)
    return [line.strip("- ").strip() for line in output_lines if line.strip()]

# Sample usage
df['rephrased_rules'] = df['split_rules'].apply(gpt_rephrase_row)