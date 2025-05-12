def summarize_comments(self, df):
    summaries = []
    prompt_template = PROMPTS.get(self.business_division, PROMPTS["DEFAULT"])['prompt']

    for _, row in df.iterrows():
        original_comment = row['COMMENT']

        # Send the full structured comment to the LLM in one go
        prompt = prompt_template.format(comments=original_comment.strip())
        response = self.llm.invoke(prompt)
        summary = response.content if hasattr(response, "content") else str(response)

        updated_row = row.to_dict()
        updated_row["COMMENT"] = summary.strip()
        updated_row["CREATED_BY"] = "AI_Generated"
        updated_row["CREATED_ON"] = datetime.now().strftime("%d/%m/%Y %H:%M")

        summaries.append(updated_row)

    return pd.DataFrame(summaries)


"prompt": (
    "You are a financial analyst. The following text contains commentary divided into sections, each beginning with a title like "
    "'Investment Banking:', 'Personal & Cooperation:', etc.\n\n"
    "Summarize each section separately, preserving the original titles.\n"
    "Return the output in the format:\n"
    "<li><strong>Title</strong> Summary of that section</li>\n"
    "Use '\\n' to separate each item. Do not merge content from different sections. Do not include explanations or extra text.\n\n"
    "{comments}"
)

################   2     #################

def summarize_comments(self, df, batch_size=3000):
    summaries = []
    prompt_template = PROMPTS.get(self.business_division, PROMPTS["DEFAULT"])['prompt']

    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i + batch_size]
        
        # Combine comments for the batch with clear separators
        combined_comments = "\n".join(batch_df["COMMENT"].dropna().tolist())

        # Format the prompt
        prompt = prompt_template.format(comments=combined_comments)

        # Call LLM once per batch
        response = self.llm.invoke(prompt)
        summary_content = response.content if hasattr(response, "content") else str(response)

        # Assign the same summary back to each row (if keeping structure), or create one summary row
        summary_row = batch_df.iloc[0].to_dict()
        summary_row.update({
            "COMMENT": summary_content,
            "LEAF_FUNC_DESC": "Summary",
            "CREATED_BY": "AI_Generated",
            "CREATED_ON": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        summaries.append(summary_row)

    return pd.DataFrame(summaries)


PROMPTS = {
    "GF": {
        "prompt": (
            "Below are multiple financial commentary sections, each starting with a business title "
            "(like 'Investment Banking:', 'Personal & Cooperation:', etc.). "
            "Summarize each section **separately**, keeping the title intact. "
            "Return the output as HTML list items, each in the format:\n"
            "<li><strong>Title:</strong> Summary.</li>\n\n"
            "Commentary:\n{comments}"
        ),
        "output_table": "etl.frs_gf"
    },
    ...
}
