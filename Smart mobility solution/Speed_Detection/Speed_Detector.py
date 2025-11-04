from ultralytics import YOLO
import pandas as pd


class VehicleDetector:
    """
    Detects vehicles in a given video frame using a YOLO model.
    """

    def __init__(self, model_path: str = "yolov9c.pt", class_list: list[str] | None = None):
        """
        Initialize the VehicleDetector with a YOLO model and class filter.

        Args:
            model_path (str): Path to the YOLO model file.
            class_list (list[str] | None): List of class names to detect.
                Defaults to ['car', 'bus', 'truck', 'motorcycle'].
        """
        self.model = YOLO(model_path)
        self.class_list = class_list or ["car", "bus", "truck", "motorcycle"]

    def detect(self, frame) -> list[list[int]]:
        """
        Perform vehicle detection on a given frame.

        Args:
            frame (np.ndarray): The video frame for object detection.

        Returns:
            list[list[int]]: A list of bounding boxes [x1, y1, x2, y2] for detected vehicles.
        """
        results = self.model.predict(frame)
        detections = []

        if not results or not hasattr(results[0], "boxes") or results[0].boxes.data is None:
            return detections  # Return empty list if no detection

        data = results[0].boxes.data.cpu().numpy()
        df = pd.DataFrame(data).astype(float)

        for _, row in df.iterrows():
            x1, y1, x2, y2, _, cls_id = row
            cls_id = int(cls_id)

            if cls_id < len(self.model.names):
                cls_name = self.model.names[cls_id]
                if cls_name in self.class_list:
                    detections.append([int(x1), int(y1), int(x2), int(y2)])

        return detections
