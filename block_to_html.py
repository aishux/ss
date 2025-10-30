import re
import html

data = """<paste your full text here>"""

blocks = re.split(r'Block Number:\s*\d+:', data)
html_blocks = []

for block in blocks:
    if not block.strip():
        continue
    
    # Extract text and formatting
    text_match = re.search(r'Text:\s*(.*?)(?:Formatting|<|$)', block, re.S)
    font_match = re.search(r'Font:\s*([A-Za-z0-9 ]+)', block)
    size_match = re.search(r'Size:\s*([\d.]+)', block)
    color_match = re.search(r'Colour:\s*(\d+)', block)
    
    text = html.escape(text_match.group(1).strip()) if text_match else ""
    font = font_match.group(1).strip() if font_match else "Arial"
    size = float(size_match.group(1)) if size_match else 12
    color = f"#{int(color_match.group(1)):06x}" if color_match else "#000000"
    
    # Build styled span
    styled_text = f'<p style="font-family:{font}; font-size:{size}px; color:{color};">{text}</p>'
    html_blocks.append(styled_text)

html_content = "<html><body>" + "\n".join(html_blocks) + "</body></html>"

with open("output.html", "w", encoding="utf-8") as f:
    f.write(html_content)
