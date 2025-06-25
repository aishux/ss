from langchain_openai import AzureChatOpenAI

# Initialize Azure OpenAI model
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

    user_prompt = f"""
You are a Rephrasing assistant that rewrites business rules into clear, human-readable English.

Rewrite the following rules into clear English sentences:
{rules_text}
"""

    response = llm.invoke([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_prompt}
    ])

    # Extract and clean the content
    output_lines = response.content.split("\n")
    return [line.strip("-• ").strip() for line in output_lines if line.strip()]

# Example usage with a DataFrame
import pandas as pd

# Assume synonyms already replaced
df = pd.DataFrame({
    "split_rules": [
        ["Current year for this year will be high", "GWM performance has grown"],
        ["Resources are insufficient this quarter"]
    ]
})

# Apply the LLM function
df['rephrased_rules'] = df['split_rules'].apply(rewrite_rules_with_llm)

# View result
print(df[['split_rules', 'rephrased_rules']])


Always maintain the abbreviations case 
In each point, split it into actionable sub points
Consider each point as a separate entity and wherever a previous context is used, add the detailed steps again in that point. 
