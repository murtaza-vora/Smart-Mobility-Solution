import os
import cv2


def ensure_folder(folder: str) -> None:
    """
    Ensure that the specified folder exists. If it doesn't, create it.

    Args:
        folder (str): Path to the folder to check or create.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)


def save_frame(frame, folder: str, frame_id: int) -> None:
    """
    Save a single video frame as an image file.

    Args:
        frame (np.ndarray): The video frame to save.
        folder (str): The folder path where the image will be stored.
        frame_id (int): The frame number used in the image filename.
    """
    filename = os.path.join(folder, f"frame_{frame_id}.jpg")
    cv2.imwrite(filename, frame)
