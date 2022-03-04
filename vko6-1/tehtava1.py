import requests
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.storage.blob import BlobClient
from azure.storage.blob import BlobServiceClient
from azure.identity import AzureCliCredential
import os
import time


credential = AzureCliCredential()
subscription_id = os.environ["SUBSCRIPTION_ID"]
kayttajanimi = str(input("Anna nimesi, resursseille luodaan nimet sen mukaan: "))
GROUP_NAME = f"{kayttajanimi}RG"
STORAGE_ACCOUNT = f"{kayttajanimi}stordemo"
BLOB_CONTAINER = f"{kayttajanimi}blobstorage"

storage_client = StorageManagementClient(credential, subscription_id)
resource_client = ResourceManagementClient(credential, subscription_id)

def request():
    r = requests.get("https://2ri98gd9i4.execute-api.us-east-1.amazonaws.com/dev/academy-checkpoint2-json")
    sisaltojson = r.json()

    with open("checkpoint.txt", "a") as checkpoint:
        for i in sisaltojson["items"]:
            checkpoint.write(i['parameter'] + "\n")

def createrg():
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "westeurope"})



def createblobcont():
    # Create blob container
    blob_container = storage_client.blob_containers.create(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        BLOB_CONTAINER,
        {}
    )

def createstorageacc():
    # Create storage account
    storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE_ACCOUNT,
        {
            "sku": {
                "name": "Standard_GRS"
            },
            "kind": "StorageV2",
            "location": "westeurope",
            "encryption": {
                "services": {
                    "file": {
                        "key_type": "Account",
                        "enabled": True
                    },
                    "blob": {
                        "key_type": "Account",
                        "enabled": True
                    }
                },
                "key_source": "Microsoft.Storage"
            },
            }
    )

def uploadfile():
    MY_CONNECTION_STRING = str(input("Anna connection string Blob containeriin: "))
    BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
    blob = BlobClient.from_connection_string(MY_CONNECTION_STRING, BLOB_CONTAINER, "checkpoint.txt")
    with open("checkpoint.txt", "rb") as data:
        blob.upload_blob(data)

print("Ohjelma luo RG:n")
createrg()
print("Ohjelma odottaa 10 sec, jotta RG on varmasti luotu")
time.sleep(10)
print("Ohjelma luo Storage Accountin")
createstorageacc()
print("Ohjelma odottaa 30 sec, jotta Storage Account on varmasti luotu")
time.sleep(30)
print("Ohjelma luo Blob Storage Containerin")
createblobcont()
uploadfile()