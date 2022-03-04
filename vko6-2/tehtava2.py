import argparse
import os
import os.path
import time

from azure.identity import AzureCliCredential
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobClient, BlobServiceClient

credential = AzureCliCredential()
subscription_id = os.environ["SUBSCRIPTION_ID"]
storage_client = StorageManagementClient(credential, subscription_id)
print("Ohjelma olettaa, että resurssit on luotu tehtävä 1:n ohjelmalla!")
kayttajanimi = str(input("Anna nimesi, tiedosto ladataan nimet sen mukaan: "))
GROUP_NAME = f"{kayttajanimi}RG"
STORAGE_ACCOUNT = f"{kayttajanimi}stordemo"
BLOB_CONTAINER = f"{kayttajanimi}blobstorage"

# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('x', type=int)
# Parse the argument
args = parser.parse_args()
#args.kerrat

def downloadfile():
    MY_CONNECTION_STRING = str(input("Anna connection string Blob containeriin: "))
    BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
    blob = BlobClient.from_connection_string(MY_CONNECTION_STRING, BLOB_CONTAINER, "checkpoint.txt")
    with open("checkpoint.txt", "wb") as my_blob:
        blob_data = blob.download_blob()
        blob_data.readinto(my_blob)
    print(f"Ladattu tiedosto")

uudetlinjat = []


def readfile():
    while not os.path.exists(os.path.realpath("checkpoint.txt")):
        time.sleep(1)

    if os.path.isfile(os.path.realpath("checkpoint.txt")):
        f = open("checkpoint.txt", "r")
    
        linjat = f.readlines()
        a = sorted(linjat)
        for x in range(args.x):
            print (a[x])



downloadfile()
readfile()
