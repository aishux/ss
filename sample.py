import re

# Sample words with alphabets and numbers
words = ["1abc2", "3xyzsh7skks", "8jkdkd"]

# Function to extract numbers and calculate their sum
def extract_and_sum(numbers):
    total_sum = 0
    for word in numbers:
        extracted_numbers = re.findall(r'\d+', word)  # Extract numbers using regex
        if len(extracted_numbers) == 1:
            num = int(extracted_numbers[0])
            total_sum += num * 2  # Consider one number twice
        elif len(extracted_numbers) >= 2:
            num1 = int(extracted_numbers[0])
            num2 = int(extracted_numbers[1])
            total_sum += num1 + num2

    return total_sum

result = extract_and_sum(words)
print("The sum of the extracted numbers:", result)
