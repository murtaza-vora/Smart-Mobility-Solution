import os
import requests
import logging
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_confirm_token(response: requests.Response) -> Optional[str]:
    """
    Retrieve the Google Drive confirmation token from response cookies.

    Args:
        response (requests.Response): The response object from Google Drive.

    Returns:
        Optional[str]: The confirmation token if found, otherwise None.
    """
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    return None


def save_response_content(response: requests.Response, dest_path: str) -> None:
    """
    Save streamed file content from response to the destination path.

    Args:
        response (requests.Response): The HTTP response containing file data.
        dest_path (str): Path to save the downloaded file.
    """
    chunk_size = 32768
    with open(dest_path, "wb") as file:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                file.write(chunk)


def download_file_from_google_drive(file_id: str, dest_path: str) -> None:
    """
    Download a file from Google Drive using its file ID.

    Args:
        file_id (str): The unique file ID from Google Drive share link.
        dest_path (str): Local path where the file should be saved.

    Raises:
        ValueError: If the download fails or the file is incomplete.
    """
    if os.path.exists(dest_path):
        logging.info("File already exists at %s", dest_path)
        return

    url = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(url, params={"id": file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": file_id, "confirm": token}
        response = session.get(url, params=params, stream=True)

    save_response_content(response, dest_path)

    if os.path.exists(dest_path):
        logging.info("✅ File downloaded successfully!")
    else:
        raise ValueError("❌ Error occurred while downloading the file.")
