from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobServiceClient

subscription_id = '4c4786a8-9501-4066-910e-6ead1624a7a5'
resource_group_name = 'MyResourceGroup'
location = 'eastus' 
storage_account_name = 'vphan03' 
container_name = 'mycontainer'

credential = DefaultAzureCredential()

resource_client = ResourceManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)

print(f"Creating resource group: {resource_group_name}...")
resource_client.resource_groups.create_or_update(resource_group_name, {'location': location})

print(f"Creating storage account: {storage_account_name}...")
storage_async_poller = storage_client.storage_accounts.begin_create(
    resource_group_name,
    storage_account_name,
    {
        'sku': {'name': 'Standard_LRS'},
        'kind': 'StorageV2',
        'location': location
    }
)
storage_account = storage_async_poller.result()  

print("Retrieving storage account keys...")
keys = storage_client.storage_accounts.list_keys(resource_group_name, storage_account_name)
storage_keys = {v.key_name: v.value for v in keys.keys}
storage_account_key = storage_keys['key1']

blob_service_client = BlobServiceClient(
    f"https://{storage_account_name}.blob.core.windows.net",
    credential=storage_account_key
)

print(f"Creating blob container: {container_name}...")
blob_service_client.create_container(container_name)

print(f"Azure Blob Storage and container '{container_name}' created successfully!")
