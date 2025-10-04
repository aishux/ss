import json

async def content_validator(self, response_template, ai_response_content):
    print("################ RESPONSE TEMPLATE ################")
    print(response_template)

    async def evaluate(ai_response):
        """Ask AI to evaluate formatting correctness."""
        eval_prompt = """
        You are an evaluator. Check if the generated content matches the expected formatting exactly as mentioned in the instructions template. The content doesn't need to match but the formatting rules need to be followed.

        Expected formatting rules: {response_template}
        
        Generated Content:
        {ai_response}
        
        Return ONLY a JSON object (no extra text) in below format as it will be directly put into json.loads method:
        {{
          "Status": "pass" if the generated content strictly matches the formatting instructions or "fail" if otherwise,
          "Comment": "<brief analysis about something which is not matching the formatting rules and how to correct it >"
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
        Your goal is to format the generated content exactly as per the rules mentioned in the formatting template below.
        
        Formatting rules template:
        {response_template}

        Original generated content:
        {ai_response_content}

        Return only the corrected content (not an explanation) as per the formatting rules. 
        The content doesn't need to match but the formatting rules need to be followed.
        """
        
        updated_response = await self.invoke_commentary_llm(
            prompt_template=feedback_prompt,
            prompt_inputs={"response_template": response_template, "ai_response_content": ai_response_content, "failed_comment": failed_comment}
        )

        ai_response_content = updated_response.content


    # ❌ after 3 attempts → return fail
    return ai_response_content
