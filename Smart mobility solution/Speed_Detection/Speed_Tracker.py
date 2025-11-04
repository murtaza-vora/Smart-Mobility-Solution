import math


class Tracker:
    """
    Tracks multiple objects across video frames using simple centroid tracking.
    Each detected object is assigned a unique ID that persists across frames.
    """

    def __init__(self) -> None:
        """Initialize the tracker with empty state."""
        self.center_points: dict[int, tuple[int, int]] = {}
        self.id_count: int = 0

    def update(self, objects_rect: list[list[int]]) -> list[list[int]]:
        """
        Update tracked objects based on new detections.

        Args:
            objects_rect (list[list[int]]): List of bounding boxes as [x, y, w, h].

        Returns:
            list[list[int]]: Updated list of bounding boxes with IDs as [x, y, w, h, id].
        """
        objects_bbs_ids: list[list[int]] = []

        # Iterate through all detected objects
        for rect in objects_rect:
            x, y, w, h = rect
            cx, cy = int((x + w) / 2), int((y + h) / 2)

            same_object_detected = False

            # Compare with existing tracked objects
            for object_id, prev_center in self.center_points.items():
                dist = math.hypot(cx - prev_center[0], cy - prev_center[1])

                # If the object is close enough, consider it the same
                if dist < 25:
                    self.center_points[object_id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, object_id])
                    same_object_detected = True
                    break

            # Register new object if not detected before
            if not same_object_detected:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Update dictionary to keep only current frame's active objects
        new_center_points: dict[int, tuple[int, int]] = {}
        for _, _, _, _, object_id in objects_bbs_ids:
            new_center_points[object_id] = self.center_points[object_id]

        self.center_points = new_center_points.copy()
        return objects_bbs_ids
