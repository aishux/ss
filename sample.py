from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential

# Replace with your actual values
search_service_name = "your-search-service-name"
index_name = "your-index-name"
api_key = "your-admin-key"
endpoint = f"https://{search_service_name}.search.windows.net"

# Initialize the SearchIndexClient
index_client = SearchIndexClient(endpoint=endpoint,
                                 credential=AzureKeyCredential(api_key))

# Get the index definition
index = index_client.get_index(index_name)

# Print all field names and their properties
print(f"📘 Fields in index '{index_name}':\n")
for field in index.fields:
    print(f"Name: {field.name}")
    print(f"  Type: {field.type}")
    print(f"  Searchable: {field.searchable}")
    print(f"  Filterable: {field.filterable}")
    print(f"  Sortable: {field.sortable}")
    print(f"  Facetable: {field.facetable}")
    print(f"  Key: {field.key}")
    print()

 
