import cv2


def draw_lines(frame, red_line_y, blue_line_y):
    """
    Draw red and blue horizontal lines on the frame.

    Args:
        frame (np.ndarray): The image/frame to draw lines on.
        red_line_y (int): Y-coordinate for the red line.
        blue_line_y (int): Y-coordinate for the blue line.
    """
    cv2.line(frame, (0, red_line_y), (frame.shape[1], red_line_y), (0, 0, 255), 2)
    cv2.line(frame, (0, blue_line_y), (frame.shape[1], blue_line_y), (255, 0, 0), 2)


def draw_info(frame, speed, bbox, object_id):
    """
    Draw bounding box, object ID, and speed information on the frame.

    Args:
        frame (np.ndarray): The image/frame to draw information on.
        speed (float): The object's speed in km/h.
        bbox (tuple): Bounding box coordinates as (x1, y1, x2, y2).
        object_id (int): Unique identifier for the object.
    """
    x1, y1, x2, y2 = bbox

    # Draw bounding box
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Draw object ID
    cv2.putText(
        frame,
        f"ID {object_id}",
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
    )

    # Draw speed if available
    if speed:
        cv2.putText(
            frame,
            f"{int(speed)} km/h",
            (x2, y2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )
