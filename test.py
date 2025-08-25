import re
from PyPDF2 import PdfReader

reader = PdfReader("template.pdf")
response_template = ""
for page in reader.pages:
    text = page.extract_text()

    # Fix case where sentences get glued (period followed by space + capital letter/word)
    text = re.sub(r"(?<=\.)\s+([A-Z])", r"\n\n\1", text)

    # Normalize multiple newlines (preserve original paragraph spacing)
    text = re.sub(r"\n{3,}", "\n\n", text)

    response_template += text.strip() + "\n\n"  # ensure separation between pages

print(response_template)
