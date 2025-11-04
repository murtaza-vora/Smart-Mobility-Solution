import cv2
from typing import Dict, Tuple


def draw_lines_and_labels(frame: "np.ndarray", line_coords: Dict[str, Dict[str, Tuple[int, int] | str]]) -> None:
    """
    Draw directional lines and their labels on the frame.

    Args:
        frame (np.ndarray): The video frame on which to draw.
        line_coords (dict): Dictionary with line information.
            Example format:
            {
                "up": {"start": (x1, y1), "end": (x2, y2), "label": "Up Line"},
                "down": {"start": (x3, y3), "end": (x4, y4), "label": "Down Line"}
            }
    """
    red = (0, 0, 255)
    text_color = (255, 255, 0)

    for direction, line in line_coords.items():
        start = line["start"]
        end = line["end"]
        label = line["label"]

        cv2.line(frame, start, end, red, 3)
        cv2.putText(
            frame,
            label,
            (start[0] - 100, start[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            text_color,
            1,
        )


def draw_vehicle_count(frame: "np.ndarray", counts: Dict[str, int]) -> None:
    """
    Display vehicle counts for each direction on the frame.

    Args:
        frame (np.ndarray): The video frame on which to draw.
        counts (dict): Dictionary with vehicle counts per direction.
            Example: {"up": 5, "down": 7}
    """
    red = (0, 0, 255)
    y_position = 40

    for direction, count in counts.items():
        cv2.putText(
            frame,
            f"{direction} Vehicles: {count}",
            (60, y_position),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            red,
            1,
        )
        y_position += 30
