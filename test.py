from bs4 import BeautifulSoup

async def your_function(self, prompt_template, summarization_template_input, response_template):
    print("################ RESPONSE TEMPLATE ################")
    print(response_template)

    def compare_templates(ai_html, expected_template):
        soup = BeautifulSoup(ai_html, "html.parser")
        ai_styles = []

        for tag in soup.find_all():
            style = tag.get("style", "")
            ai_styles.append({
                "tag": tag.name,
                "text": tag.get_text(strip=True),
                "style": style
            })

        mismatches = []
        for expected in expected_template.get("styles", []):
            match = next(
                (a for a in ai_styles if a["text"] == expected["text"]),
                None
            )
            if not match:
                mismatches.append(f"Missing text: {expected['text']}")
                continue

            if expected["font"] not in match["style"]:
                mismatches.append(f"Font mismatch for '{expected['text']}'")

            if expected["color"] not in match["style"]:
                mismatches.append(f"Color mismatch for '{expected['text']}'")

        if mismatches:
            return False, "; ".join(mismatches)
        return True, "All fonts, colors, and headings match perfectly."

    # Retry evaluator loop (max 3 times)
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        ai_response_template = await self.invoke_commentary_llm(
            prompt_template=prompt_template,
            prompt_inputs=summarization_template_input
        )

        ai_html = ai_response_template.content
        status, comment = compare_templates(ai_html, response_template)

        if status:
            return {"Status": "pass", "Comment": comment, "Output": ai_html}
        else:
            if attempt < max_retries:
                continue
            return {"Status": "fail", "Comment": comment, "Output": ai_html}