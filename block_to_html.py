import re
import html

# Paste your raw text here
raw_text = """<your full data>"""

# Split into blocks
blocks = re.split(r'Block Number:\s*\d+:', raw_text)
html_blocks = []

for block in blocks:
    block = block.strip()
    if not block:
        continue

    # Find all segments like: Text: ... Formatting Instructions ...
    segments = re.findall(
        r'Text:\s*(.*?)(?=(?:Formatting|Block Number:|$))',
        block, re.S
    )

    # Find all formatting details (in same order as texts)
    formats = re.findall(
        r'Font:\s*([A-Za-z0-9 ]+)(?:,\s*(Bold|Italic))?.*?Size:\s*([\d.]+)\s*\|\s*Colour:\s*(\d+)',
        block
    )

    html_segment_texts = []
    for i, text in enumerate(segments):
        text = text.strip()
        if not text:
            continue

        # Fallbacks if formatting missing
        if i < len(formats):
            font, style, size, color = formats[i]
        else:
            font, style, size, color = "Aptos", "", "12.0", "0"

        color_hex = f"#{int(color):06x}"  # convert int to hex color
        style_attr = f"font-family:{font}; font-size:{size}px; color:{color_hex};"
        if "Bold" in style:
            style_attr += " font-weight:bold;"
        if "Italic" in style:
            style_attr += " font-style:italic;"

        html_segment_texts.append(f'<span style="{style_attr}">{html.escape(text)}</span>')

    # Combine all segments for this block into one <p>
    block_html = "<p>" + " ".join(html_segment_texts) + "</p>"
    html_blocks.append(block_html)

# Combine into full HTML document
html_content = "<html><body>\n" + "\n".join(html_blocks) + "\n</body></html>"

# Save output
with open("output_formatted.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Formatted HTML created: output_formatted.html")
