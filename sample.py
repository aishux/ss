def summarize_comments(self, df):
    summaries = []
    prompt_template = PROMPTS.get(self.business_division, PROMPTS["DEFAULT"])['prompt']

    clubbed_comments = []
    batch_rows = []
    MAX_PER_BATCH = 500

    for _, row in df.iterrows():
        clubbed_comments.append(row['COMMENT'].strip())
        batch_rows.append(row.to_dict())

        # once we hit 500 comments, or at end of df
        if len(clubbed_comments) == MAX_PER_BATCH:
            # 1) build prompt for the batch
            prompt = prompt_template.format(comments="\n".join(clubbed_comments))

            # 2) call the LLM
            response = self.llm.invoke(prompt)
            text = getattr(response, "content", str(response))
            summary_lines = [s.strip() for s in text.split("\n") if s.strip()]

            # 3) map each summary line back to the corresponding original row
            for original, summary in zip(batch_rows, summary_lines):
                updated = original.copy()
                updated["COMMENT"] = summary
                updated["CREATED_BY"] = "AI_Generated"
                updated["CREATED_ON"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                summaries.append(updated)

            # 4) reset for the next batch
            clubbed_comments = []
            batch_rows = []

    # Handle the last partial batch (if any remain)
    if clubbed_comments:
        prompt = prompt_template.format(comments="\n".join(clubbed_comments))
        response = self.llm.invoke(prompt)
        text = getattr(response, "content", str(response))
        summary_lines = [s.strip() for s in text.split("\n") if s.strip()]

        for original, summary in zip(batch_rows, summary_lines):
            updated = original.copy()
            updated["COMMENT"] = summary
            updated["CREATED_BY"] = "AI_Generated"
            updated["CREATED_ON"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            summaries.append(updated)

    return pd.DataFrame(summaries)



"prompt": (
    "You are a financial analyst. The following text contains commentary divided into sections, each beginning with a title like "
    "'Investment Banking:', 'Personal & Cooperation:', etc.\n\n"
    "Summarize each section separately, preserving the original titles.\n"
    "Return the output in the format:\n"
    "<li><strong>Title</strong> Summary of that section</li>\n"
    "Use '\\n' to separate each item. Do not merge content from different sections. Do not include explanations or extra text.\n\n"
    "Below are the 500 comments each seperated by '\\n' and you have to output the summarizations for each section as per the given format above and seperated by '\\n' without any extra explanation\n\n"
    "{comments}"
)
