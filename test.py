from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient

# Replace with your Key Vault name
key_vault_url = "https://<your-key-vault-name>.vault.azure.net/"

# Authenticate and create client
credential = DefaultAzureCredential()
key_client = KeyClient(vault_url=key_vault_url, credential=credential)

# List all keys in the Key Vault
print("Listing keys:")
keys = key_client.list_properties_of_keys()
for key_prop in keys:
    print(f"- {key_prop.name}")

# Get a specific key (replace with an actual key name)
key_name = "<your-key-name>"
key = key_client.get_key(key_name)

print("\nKey details:")
print(f"Name: {key.name}")
print(f"Type: {key.key_type}")
print(f"Version: {key.properties.version}")
