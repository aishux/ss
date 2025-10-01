import re
from bs4 import BeautifulSoup

async def your_function(self, prompt_template, summarization_template_input, response_template):
    print("################ RESPONSE TEMPLATE ################")
    print(response_template)

    def compare(ai_html, response_template_str):
        # Parse response_template raw string
        expected_styles = []
        pattern = r"Text:\s*(.*?)\s*\|\s*Font:\s*([\w,]+).*?\|\s*Colour:\s*(\d+)"
        for match in re.finditer(pattern, response_template_str, re.DOTALL):
            text, font, color = match.groups()
            expected_styles.append({"text": text.strip(), "font": font.strip(), "color": color.strip()})

        # Extract AI styles from HTML
        soup = BeautifulSoup(ai_html, "html.parser")
        ai_styles = [{"text": t.get_text(strip=True), "style": t.attrs.get("style", "")}
                     for t in soup.find_all()]

        # Compare
        mismatches = []
        for expected in expected_styles:
            match = next((a for a in ai_styles if expected["text"] in a["text"]), None)
            if not match:
                mismatches.append(f"Missing text: {expected['text']}")
                continue
            if expected["font"].lower() not in match["style"].lower():
                mismatches.append(f"Font mismatch for '{expected['text']}'")
            if expected["color"] not in match["style"]:
                mismatches.append(f"Color mismatch for '{expected['text']}'")

        return (len(mismatches) == 0, "; ".join(mismatches) if mismatches else "All match")

    # Retry loop (max 2 times)
    for attempt in range(1, 3):
        ai_response_template = await self.invoke_commentary_llm(
            prompt_template=prompt_template,
            prompt_inputs=summarization_template_input
        )
        ai_html = ai_response_template.content
        status, comment = compare(ai_html, response_template)

        if status:   # ✅ pass → return HTML directly
            return ai_html
        elif attempt == 2:  # ❌ fail after 2 retries
            return {"Status": "fail", "Comment": comment, "Output": ai_html}