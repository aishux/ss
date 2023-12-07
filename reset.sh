#!/bin/bash

# JSON data as a string within the script
json_data='
{
  "name": "John Doe",
  "age": 30,
  "email": "john@example.com",
  "address": {
    "street": "123 Main St",
    "city": "Anytown",
    "country": "USA"
  }
}
'

# Store the entire JSON data in a variable
all_data="$json_data"

# Print the entire JSON data stored in the variable
echo "All Data: $all_data"
