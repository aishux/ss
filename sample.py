# Function to extract numbers and calculate their sum
def extract_and_sum(words):
    total_sum = 0
    for word in words:
        left_pointer = 0
        right_pointer = len(word) - 1
        left_number = ''
        right_number = ''

        # Find the leftmost number
        while left_pointer < len(word):
            if word[left_pointer].isdigit():
                left_number += word[left_pointer]
                break
            left_pointer += 1

        # Find the rightmost number
        while right_pointer >= 0:
            if word[right_pointer].isdigit():
                right_number = word[right_pointer] + right_number
                break
            right_pointer -= 1

        # Concatenate and add numbers to the total sum
        if left_number and right_number:
            total_sum += int(left_number + right_number)
        elif left_number:
            total_sum += int(left_number) * 2  # Consider single number twice

    return total_sum

# Read words from a file where each word is on a separate line
file_path = 'path_to_your_file.txt'  # Replace with the actual file path
with open(file_path, 'r') as file:
    words = file.read().splitlines()

result = extract_and_sum(words)
print("The sum of the extracted numbers:", result)
