import re
import html
import html2text

# ⚠️ YOUR FULL DATA: Paste your full data here
raw_text = """
Block Number: 1: Text: Results: 2Q24 vs 2Q23 I Formatting Instructions- ]Text : I Formatting_Instructions- [Font: Aptos [ront: Aptos, Bold | Size: 15.960000038146973 | Colour: 16711680 | Size: 15.960000038146973 | Colour: 16711680 ] ＜Or＞
Block Number: 2: Text: Profit before tax was USD 477m, mainly due to higher total revenues, partly offset by higher Formatting Instructions- 一 [Font: Aptos I Size: 12.0 | Colour: 0 ]Text: operating expenses, compared with a loss before tax of USD 121m. Underlying profit before | Formatting_ Instructions- [Font: Aptos | Size: 12.0 | Colour: 0 ]Text: tax was USD 412m, after excluding USD 310m of purchase price allocation (PPA) effects I Formatting Instructions-[Font: Aptos 1 Size: 12.0 | Colour: 0 ]Text: and USD 245m of integration-related expenses. Aptos I Size: 12.0 | Colour: 0 1 | Formatting_Instructions- [Font: ＜br>
Block Number: 3: Text: Total revenues I Formatting_Instructions- [Font: Aptos | Size: 12.0 | Colour: 16711680 ] <or>
Block Number: 4: Text: Total revenues increased by USD 767m, or 38%, to USD 2,803m, due to higher Global | Formatting_ Instructions-[Font: Aptos | Size: 12.0 | Colour: 0 ]Text: Banking and Global Markets revenues. The consolidation of Credit Suisse revenues | Formatting Instructions- [Font: Aptos I Size: 12.0 | Colour: 0 ]Text: included USD 310m of PPA effects, which represented a USD 255m increase compared with USD 55m in the second quarter of 2023. Excluding these effects, underlying total Aptos | Size: 12.0 | Colour: 0 ]Text: revenues were USD 2, 493m. | Size: 12.0 | Colour: 0 ]Text: | Formatting Instructions-[Font: I Formatting_Instructions- [Font: Aptos Size: 12.0 | Colour: 0 ] <br>
Block Number: 5: Text: Global Banking | Formatting_Instructions- [Font: Aptos, Italic | Size: 12.0 | Colour: 16711680 ] <br>
Block Number: 6: Text: Global Banking revenues increased by USD 489m, or 101%, to USD 974m, including an | Formatting_ Instructions- [Font: Aptos | Size: 12.0 | Colour: 0 ]Text: increase of USD 251m of accretion of PPA adjustments on financial instruments and other | Formatting Instructions- [Font: Aptos I Size: 12.0 | Colour: 0 ]Text: PPA effects. Excluding these effects, underlying Global Banking revenues increased by USD | Formatting Instructions- [Font: Aptos I Size: 12.0 | Colour: 0 ]Text: 238m, or 55%. The overall global fee pooll,2 increased 21%. | Formatting_Instructions- [Font: | Size: 12.0 | Colour: 0 ] Aptos <or>
"""

# Split into blocks
blocks = re.split(r'Block Number:\s*\d+:', raw_text)
html_blocks = []

for block in blocks:
    block = block.strip()
    if not block:
        continue

    # Find all text segments
    segments = re.findall(
        r'Text:\s*(.*?)(?=(?:Formatting|Block Number:|$))',
        block, re.S
    )

    # Find all formatting details (same order)
    formats = re.findall(
        r'Font:\s*([A-Za-z0-9 ]+)(?:,\s*(Bold|Italic))?.*?Size:\s*([\d.]+)\s*\|\s*Colour:\s*(\d+)',
        block
    )

    # ----------------------------------------------------
    # 🚀 REVISED LOGIC: Heading Detection and Tag Assignment 🚀
    # A block is a heading if it is a single segment AND has matching formatting.
    # ----------------------------------------------------
    block_tag = "p" # Default tag is <p> (paragraph)
    
    # Check if it's a single segment with matching formatting
    if len(segments) == 1 and len(formats) >= 1:
        
        # This confirms it's a structural heading. Now determine h2 vs h4.
        
        # Perform light cleaning on the text segment for reliable keyword search
        text_content = segments[0].strip()
        text_content = re.sub(r'\s*\|\s*', ' ', text_content)
        text_content = re.sub(r'\s+', ' ', text_content)
        
        # Check for the specific keyword "Results"
        if "Results" in text_content:
            block_tag = "h2" # Use <h2> for the main "Results" heading
        else:
            block_tag = "h4" # Use <h4> for all other headings

    # ----------------------------------------------------
    
    html_segment_texts = []
    for i, text in enumerate(segments):
        text = text.strip()

        # 🧹 Clean stray pipes and extra spaces
        text = re.sub(r'\s*\|\s*', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        if not text:
            continue

        # Get formatting (fallbacks if missing)
        if i < len(formats):
            font, style, size, color = formats[i]
        else:
            # Fallback for complex text structures
            font, style, size, color = "Aptos", "", "12.0", "0"

        # ⬆️ Increase size by 4px safely
        try:
            size = float(size) + 4
        except ValueError:
            size = 16  # default fallback

        # --- 1. Build CSS Styles for the HTML Output (Ignored by Markdown) ---
        color_hex = f"#{int(color):06x}"
        style_attr = f"font-family:{font}; font-size:{size}px; color:{color_hex};"

        # We keep the CSS styles here just so the HTML output looks correct
        if "Bold" in style:
            style_attr += " font-weight:bold;"
        if "Italic" in style:
            style_attr += " font-style:italic;"
        # --------------------------------------------------------------------

        # --- 2. Build Semantic Tags for Markdown Conversion (Crucial) ---
        escaped_text = html.escape(text)
        segment_content = escaped_text

        # Use <strong> for Bold
        if "Bold" in style:
            segment_content = f'<strong>{segment_content}</strong>'
        
        # Use <em> for Italic
        if "Italic" in style:
            segment_content = f'<em>{segment_content}</em>'

        # Wrap the content in a span, applying the full CSS style
        # The <strong>/<em> inside will be preserved by html2text
        html_segment_texts.append(f'<span style="{style_attr}">{segment_content}</span>')

    # Merge all segments for this block using the determined tag (h2, h4, or p)
    block_html = f"<{block_tag}>" + " ".join(html_segment_texts) + f"</{block_tag}>"
    html_blocks.append(block_html)

# Combine all blocks into one HTML document
html_content = "<html><body>\n" + "\n".join(html_blocks) + "\n</body></html>"

# Save the formatted HTML output
with open("output_formatted_clean.html", "w", encoding="utf-8") as f:
    f.write(html_content)


# --- SECTION: Convert HTML to Markdown ---

# 1. Initialize the converter
h = html2text.HTML2Text()

# Configure the converter to prevent line wrapping and protect formatting
h.body_width = 0 
h.protect_all_italics = True 

# 2. Perform the conversion
markdown_content = h.handle(html_content)

# 3. Save the Markdown output
with open("output_converted_markdown.md", "w", encoding="utf-8") as f:
    f.write(markdown_content)


print("✅ Clean and formatted HTML created: output_formatted_clean.html")
print("✅ Converted Markdown created: output_converted_markdown.md (Headings detected, colors/fonts stripped)")
