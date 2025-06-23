pip install azure-search-documents

## List Index using Python

from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential

# Replace these with your actual values
search_service_name = "your-search-service-name"
api_key = "your-admin-key"  # Must be admin key to list indexes

# Construct endpoint
endpoint = f"https://{search_service_name}.search.windows.net"

# Create index client
index_client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

# List all indexes
indexes = index_client.list_indexes()

# Print index names
print("Available Indexes:")
for index in indexes:
    print(f"- {index.name}")

## Query Index using Python

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Replace these with your actual values
search_service_name = "your-search-service-name"
index_name = "your-index-name"
api_key = "your-query-or-admin-key"

# Construct endpoint
endpoint = f"https://{search_service_name}.search.windows.net"

# Create client
search_client = SearchClient(endpoint=endpoint,
                             index_name=index_name,
                             credential=AzureKeyCredential(api_key))

# Perform search
results = search_client.search(search_text="lake view", top=5)

# Print results
for result in results:
    print(result)
