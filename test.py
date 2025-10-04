async def your_function(self, prompt_template, summarization_template_input, response_template):
    print("################ RESPONSE TEMPLATE ################")
    print(response_template)

    async def evaluate(ai_html, response_template_str):
        """Ask AI to evaluate formatting correctness."""
        eval_prompt = f"""
        You are an evaluator. Check if the generated content matches the expected formatting exactly. 
        Expected formatting rules: {response_template}
        
        Generated Content:
        {ai_response}
        
        Return ONLY a JSON object (no extra text) in below format as it will be directly put into json.loads method:
        {{
          "Status": "pass" if the generated content strictly matches the formatting or "fail" if otherwise,
          "Comment": "<brief analysis about something which is not matching the formatting and how to correct it >"
        }}
        """
        evaluation = await self.invoke_commentary_llm(
            prompt_template=eval_prompt,
            prompt_inputs={}
        )
        return evaluation.content

    # Retry loop (max 3 times)
    for attempt in range(1, 4):
        ai_response_template = await self.invoke_commentary_llm(
            prompt_template=prompt_template,
            prompt_inputs=summarization_template_input
        )
        ai_html = ai_response_template.content

        result = await evaluate(ai_html, response_template)
        try:
            result_json = eval(result)  # or json.loads if AI outputs proper JSON
        except:
            result_json = {"Status": "fail", "Comment": "Invalid evaluation response"}

        if result_json["Status"].lower() == "pass":
            return ai_html  # ✅ pass → return final HTML

        elif attempt < 3:
            # ❌ failed → re-run with feedback
            feedback_prompt = f"""
            Fix the generated content using this feedback: {failed_comment}
            Your goal is to format the generated content exactly as per the formatting template below.
            Formatting template:
            {response_template}
    
            Original generated content:
            {ai_response_content}
    
            Return only the corrected/generated content (not an explanation).
            """
            prompt_template = feedback_prompt  # replace prompt with corrective one
        else:
            # ❌ after 3 attempts → return fail
            return {
                "Status": "fail",
                "Comment": result_json["Comment"],
                "Output": ai_html
            }
