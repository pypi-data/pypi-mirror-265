import json
import urllib.request
import zipfile
import pandas as pd
from io import StringIO, BytesIO
import pyarrow.parquet as pq
from azure.storage.blob import BlobServiceClient, ContainerClient
from typing import Optional


def upload_parquet_to_azure_storage(
    storage_account_name: str,
    storage_account_key: str,
    container: str,
    blob: str,
    df_to_upload: pd.DataFrame,
):

    # Convert Pandas DataFrame to Parquet format in memory
    parquet_stream = BytesIO()
    df_to_upload.to_parquet(parquet_stream, engine="pyarrow")
    parquet_stream.seek(0)

    # Connect to Azure Storage
    conn_str = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key}"
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)

    # Upload Parquet data to Azure Storage
    blob_client = blob_service_client.get_blob_client(container=container, blob=blob)
    blob_client.upload_blob(parquet_stream.getvalue(), overwrite=True)

    print(f"DataFrame uploaded to Azure Storage in Parquet format: {container}/{blob}")


def read_parquet_from_blob(
    storage_account_name: str,
    storage_account_key: str,
    container: str,
    blob: str,
):
    try:
        # Create BlobServiceClient
        conn_str = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key}"
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)

        # Get a client to interact with the container
        container_client = blob_service_client.get_container_client(container)

        # Get the Parquet blob as a byte stream
        blob_client = container_client.get_blob_client(blob)
        parquet_stream = BytesIO(blob_client.download_blob().readall())

        # Read Parquet byte stream into a PyArrow Table
        parquet_table = pq.read_table(parquet_stream)

        # Convert PyArrow Table to Pandas DataFrame
        df = parquet_table.to_pandas()

        return df

    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def copy_blob(
    storage_account_key: str,
    storage_account_name: str,
    source_container: str,
    source_blob: str,
    destination_container: str,
    destination_blob: str,
):
    try:
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net",
            credential=storage_account_key,
        )

        # Get source blob client
        source_blob_url = f"https://{storage_account_name}.blob.core.windows.net/{source_container}/{source_blob}"

        # Get destination blob client
        destination_blob_client = blob_service_client.get_blob_client(
            container=destination_container, blob=destination_blob
        )

        # Start copy operation
        copy_operation = destination_blob_client.start_copy_from_url(source_blob_url)

        # Wait for copy operation to complete
        copy_operation.wait()

        return (
            True,
            f"Blob '{source_blob}' copied to '{destination_blob}' successfully.",
        )
    except Exception as e:
        return False, f"Error: {str(e)}"


def get_blob_client(
    storage_account_key: str,
    container: str,
    blob: str,
    storage_account_name: Optional[str] = "fathomdatalake",
):
    connection_string = f"DefaultEndpointsProtocol=https;{storage_account_name}=storagesample;AccountName={storage_account_name};AccountKey={storage_account_key}"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container, blob=blob)
    return blob_client


def read_json_into_dict(
    storage_account_key: str,
    container: str,
    blob: str,
    storage_account_name: Optional[str] = "fathomdatalake",
):
    blob_client = get_blob_client(
        storage_account_key=storage_account_key,
        container=container,
        blob=blob,
        storage_account_name=storage_account_name,
    )
    blob_data = blob_client.download_blob().readall()
    json_data = json.loads(blob_data)
    return json_data


def write_dict_to_json(
    storage_account_key: str,
    container: str,
    blob: str,
    data_to_upload: dict,
    storage_account_name: Optional[str] = "fathomdatalake",
):
    json_data = json.dumps(data_to_upload)
    blob_client = get_blob_client(
        storage_account_key=storage_account_key,
        container=container,
        blob=blob,
        storage_account_name=storage_account_name,
    )
    blob_client.upload_blob(json_data, overwrite=True)
    print("JSON file uploaded successfully.")


def read_csv_to_pandas(
    storage_account_key: str,
    container: str,
    blob: str,
    storage_account_name: Optional[str] = "fathomdatalake",
    csv_encoding: Optional[str] = "utf-8",
):
    blob_client = get_blob_client(
        storage_account_key=storage_account_key,
        container=container,
        blob=blob,
        storage_account_name=storage_account_name,
    )
    blob_data = blob_client.download_blob().readall()
    csv_str = blob_data.decode(csv_encoding)
    csv_file = StringIO(csv_str)
    df = pd.read_csv(csv_file)
    return df


def write_pandas_df_to_csv(
    storage_account_key: str,
    container: str,
    blob: str,
    df_to_upload: pd.DataFrame,
    storage_account_name: Optional[str] = "fathomdatalake",
):
    blob_client = get_blob_client(
        storage_account_key=storage_account_key,
        container=container,
        blob=blob,
        storage_account_name=storage_account_name,
    )
    csv_str = df_to_upload.to_csv(index=False)
    blob_client.upload_blob(csv_str, overwrite=True)
    print("CSV file uploaded successfully.")


def upload_blob_from_url(
    storage_account_key: str,
    container: str,
    blob: str,
    url: str,
    storage_account_name: Optional[str] = "fathomdatalake",
):
    blob_client = get_blob_client(
        storage_account_key=storage_account_key,
        container=container,
        blob=blob,
        storage_account_name=storage_account_name,
    )
    blob_client.upload_blob_from_url(source_url=url, overwrite=True)
    print("File uploaded successfully.")


def extract_zipped_file_to_blob_dir_from_url(
    storage_account_key: str,
    container: str,
    blob_dir: str,
    zip_url: str,
    storage_account_name: Optional[str] = "fathomdatalake",
):
    connection_string = f"DefaultEndpointsProtocol=https;{storage_account_name}=storagesample;AccountName={storage_account_name};AccountKey={storage_account_key}"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    with urllib.request.urlopen(zip_url) as response:
        if response.getcode() == 200:
            with zipfile.ZipFile(BytesIO(response.read()), "r") as zip_ref:
                # Extract each file and upload it to Azure Blob Storage
                for file_info in zip_ref.infolist():
                    file_name = file_info.filename
                    file_content = zip_ref.read(file_name)
                    blob_client = blob_service_client.get_blob_client(
                        container=container, blob=blob_dir + "/" + file_name
                    )
                    blob_client.upload_blob(file_content, overwrite=True)
            print("Files uploaded successfully.")
        else:
            print("Failed to download the zip file.")


def extract_zipped_url_list_to_blob_dir(
    storage_account_key: str,
    storage_account_name: str,
    container: str,
    blob_dir: str,
    url_list: list[str],
):
    for url in url_list:
        print(url)
        extract_zipped_file_to_blob_dir_from_url(
            storage_account_key=storage_account_key,
            storage_account_name=storage_account_name,
            container=container,
            blob_dir=blob_dir + f"/{url.split('/')[-1]}",
            zip_url=url,
        )


def delete_blob_dir(
    storage_account_key: str,
    storage_account_name: str,
    container: str,
    blob_dir: str,  # with slash at end
):
    """Deletes blob directory and everything inside it for provided container, blob_dir"""
    connection_string = f"DefaultEndpointsProtocol=https;{storage_account_name}=storagesample;AccountName={storage_account_name};AccountKey={storage_account_key}"
    container_client = ContainerClient.from_connection_string(
        conn_str=connection_string, container_name=container
    )
    blobs = container_client.list_blobs(name_starts_with=blob_dir)
    for blob in blobs:
        container_client.delete_blob(blob)
    blob_dir = container_client.list_blobs(name_starts_with=blob_dir[:-1])
    for blob in blob_dir:
        container_client.delete_blob(blob)
