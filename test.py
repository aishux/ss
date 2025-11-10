# ... inside the 'for block in blocks:' loop ...

    # Find all formatting details (same order)
    formats = re.findall(
        r'Font:\s*([A-Za-z0-9 ]+)(?:,\s*(Bold|Italic))?.*?Size:\s*([\d.]+)\s*\|\s*Colour:\s*(\d+)',
        block
    )

    # ----------------------------------------------------
    # 🚀 NEW LOGIC: Heading Detection and Tag Assignment 🚀
    # ----------------------------------------------------
    block_tag = "p" # Default tag is <p> (paragraph)
    
    # A block is considered a heading if it consists of a single text segment
    if len(segments) == 1:
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
# ... (rest of the segment processing loop remains the same) ...
        # The <strong>/<em> inside will be preserved by html2text
        html_segment_texts.append(f'<span style="{style_attr}">{segment_content}</span>')

    # Merge all segments for this block using the determined tag (h2, h4, or p)
    block_html = f"<{block_tag}>" + " ".join(html_segment_texts) + f"</{block_tag}>"
    html_blocks.append(block_html)
