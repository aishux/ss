import json

async def content_validator(self, response_template, ai_response_content):
    print("################ RESPONSE TEMPLATE ################")
    print(response_template)

    async def evaluate(ai_response):
        """Ask AI to evaluate formatting correctness."""
        eval_prompt = """
        You are a strict formatting evaluator. 
        Do not evaluate the content, wording, or numbers — only the formatting structure.
        
        Expected formatting rules:
        {response_template}
        
        Generated Content:
        {ai_response}
        
        Evaluation Guidelines:
        - Only check structural formatting (e.g., headers, bullet points, bold/italic usage, paragraph separation).
        - Ignore numbers, text meaning, names, or wording differences.
        - Ignore colors, font family, or font size unless explicitly required by the rules.
        - If formatting matches exactly (even if numbers/text differ), return "pass".
        - If formatting deviates (e.g., missing bold, wrong list type, extra/missing paragraph break), return "fail".
        
        Return ONLY a JSON object (no extra text) in this format:
        {{
          "Status": "pass" or "fail",
          "Comment": "<brief reason if fail, describing which formatting rule was broken and how to correct it>"
        }}
        """
        evaluation = await self.invoke_commentary_llm(
            prompt_template=eval_prompt,
            prompt_inputs={"response_template": response_template, "ai_response": ai_response}
        )
        return evaluation.content

    # Retry loop (max 3 times)
    for attempt in range(3):

        result = await evaluate(ai_response_content)

        result = result.strip("```").strip("json")

        try:
            result_json = json.loads(result)
        except:
            result_json = {"Status": "fail", "Comment": "Invalid evaluation response"}

        if result_json["Status"].lower() == "pass":
            return ai_response_content


        # ❌ failed → re-run with feedback
        failed_comment = result_json['Comment']
        feedback_prompt = """
        Fix the generated content using this feedback: {failed_comment}
        Your goal is to format the generated content exactly as per the formatting template below.
        Formatting template:
        {response_template}

        Original generated content:
        {ai_response_content}

        Return only the corrected/generated content (not an explanation).
        """
        
        updated_response = await self.invoke_commentary_llm(
            prompt_template=feedback_prompt,
            prompt_inputs={"response_template": response_template, "ai_response_content": ai_response_content, "failed_comment": failed_comment}
        )

        ai_response_content = updated_response.content


    # ❌ after 3 attempts → return fail
    return ai_response_content
