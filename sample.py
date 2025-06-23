from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential

# Replace with your actual service details
search_service_name = "your-search-service-name"
api_key = "your-admin-key"
endpoint = f"https://{search_service_name}.search.windows.net"

# Initialize the index client
index_client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

# List synonym maps
synonym_maps = index_client.list_synonym_maps()

# Print all synonym map names and contents
print("📘 Synonym Maps in the service:\n")
for syn_map in synonym_maps:
    print(f"Name: {syn_map.name}")
    print("Synonyms:")
    print(syn_map.synonyms)
    print("-" * 50)
