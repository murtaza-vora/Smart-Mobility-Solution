import cv2
import logging
from typing import Dict, Set, Tuple
from config import FILE_ID, DEST_PATH, MODEL_PATH, CLASSES_TO_TRACK, LINE_COORDS
from utils.downloader import download_file_from_google_drive
from utils.DetectionOfFrames import load_model, detect_objects
from utils.LineVisualization import draw_lines_and_labels, draw_vehicle_count
from utils.tracker import Tracker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def is_crossing_line(
    cx: int,
    cy: int,
    line_start: Tuple[int, int],
    line_end: Tuple[int, int],
    axis: str = "horizontal",
) -> bool:
    """
    Check if the centroid crosses the defined line.

    Args:
        cx (int): Centroid x-coordinate.
        cy (int): Centroid y-coordinate.
        line_start (Tuple[int, int]): Line start coordinates.
        line_end (Tuple[int, int]): Line end coordinates.
        axis (str): Line orientation ('horizontal' or 'vertical').

    Returns:
        bool: True if centroid crosses the line, else False.
    """
    if axis == "horizontal":
        return line_start[0] < cx < line_end[0] and abs(cy - line_start[1]) < 10
    return line_start[1] < cy < line_end[1] and abs(cx - line_start[0]) < 10


def main() -> None:
    """Main function to run the traffic vehicle counter."""
    logging.info("🚗 Starting Traffic Vehicle Counter")

    # Step 1: Download video
    download_file_from_google_drive(FILE_ID, DEST_PATH)

    # Step 2: Load YOLO model
    model = load_model(MODEL_PATH)

    # Step 3: Initialize tracker and counters
    tracker = Tracker()
    counts: Dict[str, Set[int]] = {direction: set() for direction in LINE_COORDS.keys()}

    # Step 4: Process video
    cap = cv2.VideoCapture(DEST_PATH)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detect_objects(model, frame)

        # Filter only classes we want to track
        boxes = [
            [x1, y1, x2, y2]
            for x1, y1, x2, y2, _, class_id in detections
            if int(class_id) < 80 and model.names[int(class_id)] in CLASSES_TO_TRACK
        ]

        tracked_objects = tracker.update(boxes)

        for x1, y1, x2, y2, obj_id in tracked_objects:
            cx, cy = (int((x1 + x2) // 2), int((y1 + y2) // 2))

            for direction, line in LINE_COORDS.items():
                axis = "vertical" if direction == "wb" else "horizontal"
                crossed = is_crossing_line(cx, cy, line["start"], line["end"], axis=axis)

                color = (0, 255, 0)
                if crossed and obj_id not in counts[direction]:
                    counts[direction].add(obj_id)
                    color = (0, 0, 255)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        draw_lines_and_labels(frame, LINE_COORDS)
        draw_vehicle_count(frame, {k.upper(): len(v) for k, v in counts.items()})

        cv2.imshow("Traffic Counter", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()
    logging.info("✅ Processing complete!")


if __name__ == "__main__":
    main()
