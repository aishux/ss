def html_to_markdown(html):
    html = html.strip()

    # Extract inner text (very basic, assuming simple tags)
    def extract_text(tagged_str):
        result = ""
        inside_tag = False
        for ch in tagged_str:
            if ch == "<":
                inside_tag = True
            elif ch == ">":
                inside_tag = False
            elif not inside_tag:
                result += ch
        return result.strip()

    # Basic rules
    markdown_lines = []

    # Split into paragraphs
    paragraphs = html.split("</p>")
    for para in paragraphs:
        if not para.strip():
            continue

        text = extract_text(para)

        # Handle bold and italic markers
        # Handle "Results"

        print(para)

        if "Results" in text:
            text = "## " + text
        elif "bold" in para or "<b>" in para or "<strong>" in para:
            text = f"#### **{text}**"
        elif "<i>" in para or "<em>" in para or "italic" in para:
            text = f"#### *{text}*"
        markdown_lines.append(text)

    return "\n\n".join(markdown_lines)
