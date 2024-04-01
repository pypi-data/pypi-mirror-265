# catalog.py

from enum import Enum
from typing import Dict, Tuple

BASE_URLS = {
    "video": "https://media.sigmoidal.ai/video-examples/",
    "image": "https://media.sigmoidal.ai/image-examples/",
}


class MediaAsset(Enum):
    """
    Enum representing different media assets.

    Attributes:
        AIRPORT (str): The filename of the airport video asset.

    Methods:
        list_assets(): Returns a list of all media asset filenames.

    Example usage:
        asset = MediaAsset.AIRPORT
        print(asset.value)  # Output: "santos_dumont_airport.mp4"
        assets = MediaAsset.list_assets()
        print(assets)  # Output: ["santos_dumont_airport.mp4"]
    """

    AIRPORT = "santos_dumont_airport.mp4"

    @classmethod
    def list_assets(cls) -> list:
        """
        Returns a list of all media asset filenames.

        Returns:
            list: A list of media asset filenames.
        """
        return list(map(lambda x: x.value, cls))


MEDIA_ASSETS: Dict[str, Tuple[str, str]] = {
    MediaAsset.AIRPORT.value: (
        f"{BASE_URLS['video']}{MediaAsset.AIRPORT.value}",
        "b7b09d573dcf2d4035025109f43d76db",
    )
}
