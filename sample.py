from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Set env vars (or use config file)
os.environ["AZURE_OPENAI_API_KEY"] = "<your-key>"
os.environ["AZURE_OPENAI_ENDPOINT"] = "<your-endpoint>"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-05-15"

llm = AzureChatOpenAI(
    deployment_name="gpt-4",  # your Azure deployment name
    temperature=0.3
)

prompt = PromptTemplate.from_template("""
You are an assistant that rewrites business rules into clean, human-readable English.

Here are the rules:
{rules}

Rewrite each rule clearly in bullet points.
""")

chain = LLMChain(llm=llm, prompt=prompt)

# Example: row-wise in DataFrame
def rewrite_rules_with_langchain(rule_list):
    rules_text = "\n".join(f"- {r}" for r in rule_list)
    response = chain.run(rules=rules_text)
    # post-process to extract clean sentences
    return [line.strip("- ").strip() for line in response.split("\n") if line.strip()]

df['rephrased_rules'] = df['split_rules'].apply(rewrite_rules_with_langchain)