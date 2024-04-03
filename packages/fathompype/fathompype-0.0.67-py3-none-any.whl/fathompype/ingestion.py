from urllib.request import urlretrieve
import zipfile
from pathlib import Path
import os
from typing import Optional, Union
import pandas as pd


def unzip_file_to_directory(file_to_unzip: str, output_directory: str) -> None:
    with zipfile.ZipFile(file_to_unzip, "r") as zip_ref:
        zip_ref.extractall(output_directory)


def ingest_data_from_url(url: str, output_filepath: str) -> None:
    urlretrieve(url, output_filepath)
    print(f"        Dataset written to {output_filepath}!")


def unzip_file_from_url(url: str, output_directory: str) -> None:
    ingest_data_from_url(url=url, output_filepath=output_directory / "zipped_data.zip")
    print("        read zipped data")
    unzip_file_to_directory(
        file_to_unzip=output_directory / "zipped_data.zip",
        output_directory=output_directory,
    )
    print(f"        unzipped file to {output_directory}")
    Path.unlink(output_directory / "zipped_data.zip")


def ingest_data_from_url_list(
    url_list: list[str], output_directory: str, zipped: bool = False
) -> None:
    for url in url_list:
        if zipped:
            print(f"        Downloading data from {url}")
            sub_dir = url.split("/")[-1].split(".")[0]
            Path(output_directory / sub_dir).mkdir(parents=True)
            unzip_file_from_url(url=url, output_directory=output_directory / sub_dir)
        else:
            file_name = url.split("/")[-1]
            ingest_data_from_url(url=url, output_filepath=output_directory / file_name)


def read_csv(file_path: str, encoding: Optional[str] = "latin-1") -> None:
    return pd.read_csv(file_path, encoding=encoding, low_memory=False)
