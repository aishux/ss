from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential

def get_equivalent_synonyms(word, synonym_map_text):
    """
    Given a word and synonym map content, return its equivalent synonyms.
    Only handles equivalent groups (comma-separated).
    """
    word = word.lower().strip()
    synonym_lines = synonym_map_text.strip().splitlines()

    for line in synonym_lines:
        line = line.strip()

        # Skip empty or comment lines
        if not line or line.startswith("#"):
            continue

        # Skip non-equivalent types (=> or |)
        if "=>" in line or "|" in line:
            continue

        # Process comma-separated equivalent synonyms
        terms = [term.strip() for term in line.split(",")]
        terms_lower = [t.lower() for t in terms]

        if word in terms_lower:
            return [terms[i] for i in range(len(terms)) if terms_lower[i] != word]

    return []

# 🔧 Replace with your actual values
search_service_name = "your-search-service-name"
api_key = "your-admin-key"
synonym_map_name = "your-synonym-map-name"
endpoint = f"https://{search_service_name}.search.windows.net"

# 🧠 Fetch synonym map content from Azure
index_client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))
synonym_map = index_client.get_synonym_map(synonym_map_name)

# 🔍 Example usage
input_word = "MoM"
synonyms = get_equivalent_synonyms(input_word, synonym_map.synonyms)

if synonyms:
    print(f"Synonyms for '{input_word}': {synonyms}")
else:
    print(f"No synonyms found for '{input_word}'.")
