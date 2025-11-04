from typing import List


class Tracker:
    """
    Simple placeholder tracker class that assigns unique IDs to detected objects.
    """

    def __init__(self) -> None:
        """Initialize the tracker with empty objects and ID counter."""
        self.objects = {}
        self.next_id: int = 0

    def update(self, detections: List[List[int]]) -> List[List[int]]:
        """
        Update tracked objects by assigning new IDs to detections.

        Args:
            detections (List[List[int]]): List of bounding boxes [x1, y1, x2, y2].

        Returns:
            List[List[int]]: List of bounding boxes with assigned IDs [x1, y1, x2, y2, id].
        """
        tracked: List[List[int]] = []

        for det in detections:
            x1, y1, x2, y2 = det
            tracked.append([x1, y1, x2, y2, self.next_id])
            self.next_id += 1

        return tracked
