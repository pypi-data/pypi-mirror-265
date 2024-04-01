# downloader.py

import hashlib
import os
from pathlib import Path

from requests import get
from tqdm.auto import tqdm

from sigmoidalvision.assets.catalog import MEDIA_ASSETS, MediaAsset


def calculate_md5(file_path):
    """
    Calculates the MD5 hash of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The MD5 hash of the file.

    Example usage:
        md5_hash = calculate_md5("file.txt")
        print(md5_hash)  # Output: "d41d8cd98f00b204e9800998ecf8427e"
    """
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def download_media_asset(media_asset_name: MediaAsset) -> str:
    """
    Downloads a media asset from the catalog.

    Args:
        media_asset_name (MediaAsset): The name of the media asset to download.

    Returns:
        str: The filename of the downloaded media asset.

    Raises:
        ValueError: If the media asset is not available in the catalog or if there is an MD5 hash mismatch.

    Example usage:
        filename = download_media_asset(MediaAsset.AIRPORT)
        print(filename)  # Output: "santos_dumont_airport.mp4"
    """
    file_name = (
        media_asset_name.value
        if isinstance(media_asset_name, MediaAsset)
        else media_asset_name
    )

    match Path(file_name).exists(), file_name in MEDIA_ASSETS:
        case False, True:
            url, expected_md5 = MEDIA_ASSETS[file_name]
            with get(url, stream=True, allow_redirects=True) as response:
                response.raise_for_status()
                total_length = int(response.headers.get("content-length") or 0)
                with open(file_name, "wb") as file, tqdm(
                    desc="Downloading", total=total_length, unit="B", unit_scale=True
                ) as bar:
                    for data in response.iter_content(chunk_size=1024):
                        file.write(data)
                        bar.update(len(data))
            actual_md5 = calculate_md5(file_name)
            if actual_md5 != expected_md5:
                raise ValueError(
                    f"MD5 hash mismatch for {file_name}. Expected: {expected_md5}, Actual: {actual_md5}"
                )
            print(f"File {file_name} downloaded successfully.")
        case True, True:
            actual_md5 = calculate_md5(file_name)
            expected_md5 = MEDIA_ASSETS[file_name][1]
            if actual_md5 != expected_md5:
                print(
                    f"MD5 hash mismatch for {file_name}. Expected: {expected_md5}, Actual: {actual_md5}"
                )
                print(f"Removing the existing file: {file_name}")
                os.remove(file_name)
                print(f"Re-downloading the file: {file_name}")
                url, _ = MEDIA_ASSETS[file_name]
                with get(url, stream=True, allow_redirects=True) as response:
                    response.raise_for_status()
                    total_length = int(response.headers.get("content-length") or 0)
                    with open(file_name, "wb") as file, tqdm(
                        desc="Downloading",
                        total=total_length,
                        unit="B",
                        unit_scale=True,
                    ) as bar:
                        for data in response.iter_content(chunk_size=1024):
                            file.write(data)
                            bar.update(len(data))
                actual_md5 = calculate_md5(file_name)
                if actual_md5 != expected_md5:
                    raise ValueError(
                        f"MD5 hash mismatch for {file_name}. Expected: {expected_md5}, Actual: {actual_md5}"
                    )
                print(f"File {file_name} re-downloaded successfully.")
            else:
                print(
                    f"The file {file_name} already exists locally and has a matching MD5 hash."
                )
        case _, False:
            raise ValueError(
                f"The media asset {file_name} is not available in the catalog."
            )

    return file_name
