import re

with open('output.txt', 'r') as file:
    text = file.read()

pattern = r'\{([^}]*)\}'
matches = re.findall(pattern, text, re.DOTALL)

with open('extracted.txt', 'w') as ex_file:
    for match in matches:
        ex_file.write('{' + match + '}\n')

print("Extracted and saved content in 'ex_file.txt'")
