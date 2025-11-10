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

    # Extract formatting info (bold/italic)
    formats = re.findall(r'Font:\s*([A-Za-z0-9 ]+)(?:,\s*(Bold|Italic))?', block)

    md_segments = []
    for i, text in enumerate(segments):
        text = text.strip()
        text = re.sub(r'\s*\|\s*', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        if not text:
            continue

        # Detect style (if available)
        style = formats[i][1] if i < len(formats) else ""

        # Apply markdown formatting (no space inside)
        if "Bold" in style and "Italic" in style:
            text = f"***{text}***"
        elif "Bold" in style:
            text = f"**{text}**"
        elif "Italic" in style:
            text = f"*{text}*"

        md_segments.append(text)

    # Combine text in the block
    block_text = " ".join(md_segments).strip()

    # Determine if block should be heading
    # Keywords like “Results”, “Global Banking”, “Total Revenues” are headings
    if re.search(r'\bResults?\b', block_text, re.IGNORECASE):
        block_md = f"## {block_text}"
    elif re.search(r'\b(Global Banking|Total Revenues)\b', block_text, re.IGNORECASE):
        block_md = f"#### {block_text}"
    else:
        block_md = block_text  # normal paragraph

    md_blocks.append(block_md)

# Join all blocks with spacing
markdown_output = "\n\n".join(md_blocks)

# Save to file
with open("output.md", "w", encoding="utf-8") as f:
    f.write(markdown_output)

print("✅ Markdown file created: output.md")
