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


"prompt": "Summarize the following structured financial commentary while retaining the title structure:\n{comments}"
