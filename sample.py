pip install azure-search-documents

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
