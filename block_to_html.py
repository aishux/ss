import re
import html

# Paste your raw text here
raw_text = """<your full data>"""

# Step 1: Split text into blocks
blocks = re.split(r'Block Number:\s*\d+:', raw_text)

html_blocks = []

for block in blocks:
    block = block.strip()
    if not block:
        continue
    
    # Step 2: Extract all 'Text:' segments within the block
    texts = re.findall(r'Text:\s*([^|<\n]+)', block)
    
    # Step 3: Join and clean the text
    combined_text = ' '.join(t.strip() for t in texts)
    
    # Remove extra spaces and formatting junk
    combined_text = re.sub(r'\s+', ' ', combined_text)
    combined_text = html.escape(combined_text.strip())
    
    # Step 4: Wrap as HTML paragraph
    html_blocks.append(f"<p>{combined_text}</p>")

# Step 5: Combine everything into a clean HTML file
html_content = "<html><body>\n" + "\n".join(html_blocks) + "\n</body></html>"

# Step 6: Save to file
with open("output_clean.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Clean HTML created: output_clean.html")
