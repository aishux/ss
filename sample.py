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
        user_prompt = f"""
            You are a precise and structured assistant that rewrites complex business rules into clear, structured, and atomic instructions.
            
            ---
            
            ### 🔁 Task Overview:
            
            You will be given a list of business rules. Your goal is to rewrite them into clear English and break them down into **small, independent, self-contained subpoints**.
            
            Each subpoint should be:
            
            - Easy for an LLM or analyst to execute independently
            - Explicit in scope, especially when it comes to **time period comparisons**, **metrics**, or **business units**
            - Formatted using hierarchical numbering (e.g., 1.1, 1.2, or YTD-3.4)
            
            ---
            
            ### ✅ Rules to Follow:
            
            1. **Preserve original abbreviations** and casing (e.g., NPBT, DCM, F6100).
            2. **Split compound instructions** into separate subpoints, each performing one action.
            3. If a rule contains **ambiguous references** like “Do the same”, **replace** them with clear and explicit instructions derived from earlier steps.
            4. **Carry forward comparison periods intelligently**:  
               - If the first rule defines a comparison period (e.g., “current quarter vs prior quarter”), then this period applies to all subsequent subpoints **unless explicitly overridden**.
               - Make the comparison period **explicit in each subpoint** where it's relevant (e.g., “compare Revenues for the current quarter vs prior quarter”).
               - Do **not hardcode** any specific period — always infer it from the first instruction in the list.
            5. Rewrite everything in **clear business English**.
            
            ---
            
            ### 🔍 Examples:
            
            #### Input:
            > "1. Prepare a summary of Financial Performance for current quarter vs prior quarter of the same period."
            
            #### Subpoints:
            > 1.1 Prepare a summary of Financial Performance comparing the current quarter to the prior quarter of the same period.
            
            ---
            
            #### Input:
            > "2. Show the variance in Revenues and Expenses."
            
            #### Subpoints:
            > 2.1 Show the variance in Revenues over the comparison period defined in the first instruction.  
            > 2.2 Show the variance in Expenses over the same comparison period.
            
            ---
            
            #### Input:
            > "7. Do the same for YTD current year vs YTD prior year."
            
            #### Subpoints:
            > YTD-1.1 Prepare a summary of Financial Performance comparing YTD current year to YTD prior year.  
            > YTD-1.2 Highlight variance in Revenues during this YTD period.  
            > … and so on.
            
            ---
            
            Now rewrite and decompose the following rules:
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

# Now convert to readable format
df['rephrased_rules_str'] = df['rephrased_rules'].apply(lambda arr: "\n".join(arr))


# View result
print(df[['split_rules', 'rephrased_rules']])

put example
Always maintain the abbreviations case 
In each point, split it into actionable sub points
Consider each point as a separate entity and wherever a previous context is used, add the detailed steps again in that point. 
