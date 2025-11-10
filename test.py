import re

# Paste your full data here
raw_text = """<your full data>"""

# Split by block number
blocks = re.split(r'Block Number:\s*\d+:', raw_text)
md_blocks = []

for block in blocks:
    block = block.strip()
    if not block:
        continue

    # Extract all Text segments
    segments = re.findall(r'Text:\s*(.*?)(?=(?:Formatting|Block Number:|$))', block, re.S)

    # Extract formatting info
    formats = re.findall(r'Font:\s*[A-Za-z0-9 ]+(?:,\s*(Bold|Italic))?', block, re.I)

    md_segments = []
    for i, text in enumerate(segments):
        text = text.strip()
        text = re.sub(r'\s*\|\s*', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        if not text:
            continue

        # Detect style
        style = formats[i] if i < len(formats) else ""

        # Apply markdown formatting (no extra spaces)
        if "bold" in style.lower() and "italic" in style.lower():
            text = f"***{text}***"
        elif "bold" in style.lower():
            text = f"**{text}**"
        elif "italic" in style.lower():
            text = f"*{text}*"

        md_segments.append(text)

    # Combine all text in the block
    block_text = " ".join(md_segments).strip()

    # Determine heading vs paragraph
    if re.search(r'\bresults?\b', block_text, re.IGNORECASE):
        block_md = f"## {block_text}"
    elif len(block_text.split()) <= 6 and not re.search(r'\b(block|text)\b', block_text, re.I):
        # short lines are headings (e.g. Total revenues, Global Banking)
        block_md = f"#### {block_text}"
    else:
        block_md = block_text  # normal paragraph

    md_blocks.append(block_md)

# Join all blocks with spacing
markdown_output = "\n\n".join(md_blocks)
markdown_output = re.sub(r'\s+(?=[*_#])', '', markdown_output)  # remove unwanted spaces

# Save to file
with open("output.md", "w", encoding="utf-8") as f:
    f.write(markdown_output)

print("✅ Markdown file created: output.md")
