import re

# Function to extract numbers and calculate their sum
def extract_and_sum(words):
    total_sum = 0
    for word in words:
        extracted_numbers = re.findall(r'\d+', word)  # Extract numbers using regex
        if len(extracted_numbers) == 1:
            num = int(extracted_numbers[0])
            total_sum += num * 2  # Consider one number twice
        elif len(extracted_numbers) >= 2:
            num1 = int(extracted_numbers[0])
            num2 = int(extracted_numbers[1])
            total_sum += num1 + num2

    return total_sum

# Read words from a file where each word is on a separate line
file_path = 'path_to_your_file.txt'  # Replace with the actual file path
with open(file_path, 'r') as file:
    words = file.read().splitlines()

result = extract_and_sum(words)
print("The sum of the extracted numbers:", result)
