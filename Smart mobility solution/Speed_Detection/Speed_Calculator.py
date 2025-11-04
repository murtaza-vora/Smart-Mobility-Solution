import time


class SpeedEstimator:
    """
    Estimates the speed of tracked vehicles based on their crossing
    between two horizontal reference lines in the frame.
    """

    def __init__(self, red_line_y, blue_line_y, offset, distance_m=200):
        """
        Initialize the SpeedEstimator.

        Args:
            red_line_y (int): Y-coordinate of the red line.
            blue_line_y (int): Y-coordinate of the blue line.
            offset (int): Tolerance for detecting line crossing.
            distance_m (float): Real-world distance between the two lines in meters.
        """
        self.red_line_y = red_line_y
        self.blue_line_y = blue_line_y
        self.offset = offset
        self.distance_m = distance_m
        self.down = {}
        self.up = {}
        self.counter_down = []
        self.counter_up = []

    def calculate_speed(self, cy, object_id, direction):
        """
        Calculate the speed of a vehicle when it crosses the defined lines.

        Args:
            cy (int): The Y-coordinate of the object's centroid.
            object_id (int): The unique identifier of the object.
            direction (str): The movement direction ('up' or 'down').

        Returns:
            float | None: The calculated speed in km/h if measurable, else None.
        """
        current_time = time.time()

        # --- Downward direction ---
        if direction == "down":
            if self.red_line_y - self.offset < cy < self.red_line_y + self.offset:
                self.down[object_id] = current_time

            if (
                object_id in self.down
                and self.blue_line_y - self.offset < cy < self.blue_line_y + self.offset
            ):
                elapsed = current_time - self.down[object_id]
                if object_id not in self.counter_down:
                    self.counter_down.append(object_id)
                    return (self.distance_m / elapsed) * 3.6  # Convert m/s to km/h

        # --- Upward direction ---
        elif direction == "up":
            if self.blue_line_y - self.offset < cy < self.blue_line_y + self.offset:
                self.up[object_id] = current_time

            if (
                object_id in self.up
                and self.red_line_y - self.offset < cy < self.red_line_y + self.offset
            ):
                elapsed = current_time - self.up[object_id]
                if object_id not in self.counter_up:
                    self.counter_up.append(object_id)
                    return (self.distance_m / elapsed) * 3.6  # Convert m/s to km/h

        return None
