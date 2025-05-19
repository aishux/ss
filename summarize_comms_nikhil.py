import json

def summarize_comments(self, df):
    summaries = []
    prompt_template = PROMPTS.get(self.business_division, PROMPTS["DEFAULT"])['prompt']

    comment_dict = {}
    row_mapping = {}
    MAX_PER_BATCH = 500

    for idx, row in df.iterrows():
        row_id = str(row["aggregation_set"])
        comment_dict[row_id] = row["COMMENT"].strip()
        row_mapping[row_id] = row.to_dict()

        # Process when batch is full
        if len(comment_dict) == MAX_PER_BATCH:
            summaries.extend(self._process_batch(prompt_template, comment_dict, row_mapping))
            comment_dict.clear()
            row_mapping.clear()

    # Handle last partial batch
    if comment_dict:
        summaries.extend(self._process_batch(prompt_template, comment_dict, row_mapping))

    return pd.DataFrame(summaries)

def _process_batch(self, prompt_template, comment_dict, row_mapping):
    prompt = prompt_template.format(comments=json.dumps(comment_dict, indent=2))
    response = self.llm.invoke(prompt)
    text = getattr(response, "content", str(response))

    try:
        summary_dict = json.loads(text)
    except Exception as e:
        raise ValueError(f"Failed to parse LLM output: {text[:300]}...\nError: {e}")

    batch_summaries = []
    for row_id in comment_dict.keys():
        original = row_mapping.get(row_id)
        summary = summary_dict.get(row_id)

        if not summary:
            # Log missing or empty summary
            print(f"Missing or empty summary for rowId: {row_id}")
            summary = "[Summary Missing]"

        updated = original.copy()
        updated["COMMENT"] = summary
        updated["CREATED_BY"] = "AI_Generated"
        updated["CREATED_ON"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        batch_summaries.append(updated)

    return batch_summaries



"prompt": (
    "You are a financial analyst."
    "Summarize each comment, preserving the original titles.\n"
    "Return the output in the format:\n"
    "<li><strong>Title</strong> Summary of that section</li>\n"
    "Use '\\n' to separate each item. Do not merge content from different sections. Do not include explanations or extra text.\n\n"
    "Below is the dictionary of comments and you have to output the summarizations.Return the output as a single JSON object without any extra explanation\n\n"
    "{comments}"
)
