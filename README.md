import re

with open('output.txt', 'r', encoding='utf-8') as file:
    text = file.read()

matches = re.findall(r'{(.*?)}', text, re.DOTALL)

cleaned_content = []
for match in matches:
    cleaned_match = re.sub(r'[^a-zA-Z0-9\s\n]', '', match)
    cleaned_content.append('{' + cleaned_match + '}')

with open('extract.txt', 'w', encoding='utf-8') as ext_file:
    p = ext_file.write('\n'.join(cleaned_content))
    print(p)
