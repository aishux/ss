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
        You are a precise and structured assistant that rewrites complex business rules into clear, structured, and atomic instructions for implementation.
        
        Follow these instructions strictly:
        
        ---
        
        ### 🔁 Task Overview:
        
        You will be given a list of business rules (typically editorial or reporting instructions). Your goal is to **rewrite them in clearer English** and **split them into small, independent, actionable rules** that:
        
        - Can be executed without relying on previous context.
        - Each cover only **one action** or directive.
        - Are numbered hierarchically using the same rule index and subpoint pattern (e.g., 1.1, 1.2… or YTD-3.5).
        - Are grouped under sections using headings.
        - Include **no summary or commentary**, just structured output.
        
        ---
        
        ### ✅ Formatting & Style Rules:
        
        1. **Preserve all abbreviations** (e.g., NPBT, Revenues, DCM, F6100) in **exact casing** — do not expand or lowercase them.
        2. If a rule includes **"and"**, **"as well as"**, or **multiple clauses**, split it into multiple subpoints.
        3. If any rule refers to previous context (e.g., "Do the same", "Repeat above"), rewrite it with the **actual intended action** described explicitly.
        4. All points must be **clear enough** for an LLM to understand and act on **individually**.
        5. Use simple business English.
        
        ---
        
        ### 🔍 Few-shot Examples
        
        #### Input Rule:
        > "1. Highlight the variance in Revenues and Expenses that contributed to the change in NPBT."
        
        #### Output:
        > 1.1 Highlight the variance in Revenues that contributed to the change in NPBT.  
        > 1.2 Highlight the variance in Expenses that contributed to the change in NPBT.
        
        ---
        
        #### Input Rule:
        > "7. Do the exact same as Quarterly section but looking at YTD current year vs YTD prior year."
        
        #### Output:
        > YTD-1.1 Prepare a summary comparing Financial Performance for YTD current year versus YTD prior year.  
        > YTD-1.2 Include one sentence on NPBT explaining the change from YTD prior year.  
        > YTD-1.3 Highlight the variance in Revenues that contributed to the change in NPBT.  
        > … *(repeat the structure of 1–6 adapted to YTD context with subpoints)*
        
        ---
        
        Now, rewrite the following rules accordingly:
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

put example
Always maintain the abbreviations case 
In each point, split it into actionable sub points
Consider each point as a separate entity and wherever a previous context is used, add the detailed steps again in that point. 
