import json

async def content_validator(self, response_template, ai_response_content):
    print("################ RESPONSE TEMPLATE ################")
    print(response_template)

    async def evaluate(ai_response):
        """Ask AI to evaluate formatting correctness."""
        eval_prompt = """
        You are an evaluator. Check if the generated content matches the expected style formatting exactly as mentioned in the instructions template.
        
        IMPORTANT:
        
        - You are not supposed to evaluate the content just style formatting rules need to be followed.
        - The rules are to be followed for generating HTML content only not plaintext. 
        For example if the instruction is: 
        Block Number: 5: Text: Global Banking | Formatting_Instructions- [Font: Aptos | Size: 12.0 | Colour: 16711689]
        then the html for this should be <div style="font-family: Aptos; font-size: 12; color: #FF0009">Global Banking<div>
 
        Expected style formatting rules: {response_template}
        
        Generated Content:
        {ai_response}
        
        Return ONLY a JSON object (no extra text) in below format as it will be directly put into json.loads method:
        {{
          "Status": "pass" if the generated content strictly matches the style formatting instructions or "fail" if otherwise,
          "Comment": "<brief analysis about something which is not matching the style formatting rules and how to correct it >"
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
        Your goal is to format the style of generated content exactly as per the rules mentioned in the style formatting rules template below.

        Expected Style Formatting rules template:
        {response_template}

        Original generated content:
        {ai_response_content}

        IMPORTANT:
        
        - You are not supposed to evaluate the content just style formatting rules need to be followed.
        - The rules are to be followed for generating HTML content only not plaintext. 
        For example if the instruction is: 
        Block Number: 5: Text: Global Banking | Formatting_Instructions- [Font: Aptos | Size: 12.0 | Colour: 16711689]
        then the html for this should be <div style="font-family: Aptos; font-size: 12; color: #FF0009">Global Banking<div>

        Return only the corrected content (not an explanation) as per the style formatting rules. 
        """
        
        updated_response = await self.invoke_commentary_llm(
            prompt_template=feedback_prompt,
            prompt_inputs={"response_template": response_template, "ai_response_content": ai_response_content, "failed_comment": failed_comment}
        )

        ai_response_content = updated_response.content


    # ❌ after 3 attempts → return fail
    return ai_response_content
