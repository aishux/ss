async def your_function(self, prompt_template, summarization_template_input, response_template):
    print("################ RESPONSE TEMPLATE ################")
    print(response_template)

    async def evaluate(ai_html, response_template_str):
        """Ask AI to evaluate formatting correctness."""
        eval_prompt = f"""
        You are an evaluator. Check if the AI response matches the expected formatting exactly. 
        Expected formatting rules: {response_template_str}
        
        AI Response:
        {ai_html}
        
        Return ONLY a JSON object in this format:
        {{
          "Status": "pass" or "fail",
          "Comment": "<brief reason or feedback>"
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
            Fix the AI response using this feedback: {result_json['Comment']}.
            Ensure it matches these formatting rules exactly: {response_template}
            Original response:
            {ai_html}
            """
            prompt_template = feedback_prompt  # replace prompt with corrective one
        else:
            # ❌ after 3 attempts → return fail
            return {
                "Status": "fail",
                "Comment": result_json["Comment"],
                "Output": ai_html
            }