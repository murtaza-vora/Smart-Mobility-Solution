import logging
from ultralytics import YOLO
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_model(model_path: str) -> YOLO:
    """
    Load a YOLO model from the specified pretrained weights.

    Args:
        model_path (str): Path to the YOLO model file.

    Returns:
        YOLO: Loaded YOLO model ready for inference.
    """
    logging.info("Loading YOLO model from %s", model_path)
    try:
        model = YOLO(model_path)
        logging.info("Model loaded successfully.")
        return model
    except Exception as error:
        logging.error("Error loading YOLO model: %s", error)
        raise


def detect_objects(model: YOLO, frame: np.ndarray) -> np.ndarray:
    """
    Run YOLO object detection on a single frame.

    Args:
        model (YOLO): YOLO model instance for object detection.
        frame (np.ndarray): Input image or video frame.

    Returns:
        np.ndarray: Detection results as an array of bounding box data.
    """
    try:
        results = model.predict(frame)
        if not results or not hasattr(results[0], "boxes"):
            logging.warning("No detections found in the frame.")
            return np.empty((0, 6))  # Empty detection array

        return results[0].boxes.data.detach().cpu().numpy()
    except Exception as error:
        logging.error("Error during detection: %s", error)
        return np.empty((0, 6))
