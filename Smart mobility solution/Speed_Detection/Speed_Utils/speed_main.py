import cv2
from Speed_Tracker import Tracker
from Speed_Detector import VehicleDetector
from Speed_Calculator import SpeedEstimator
from utils.Pixel_Point import draw_lines, draw_info
from utils.Frames_Folder import ensure_folder, save_frame


def main():
    """
    Main function to perform vehicle detection, tracking, and speed estimation
    from a video source.
    """
    # --- Setup ---
    video_path = "/content/drive/MyDrive/murru5 (1).mp4"
    red_line_y, blue_line_y, offset = 120, 80, 6

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Error: Unable to open video file {video_path}")

    detector = VehicleDetector()
    tracker = Tracker()
    speed_estimator = SpeedEstimator(red_line_y, blue_line_y, offset)

    ensure_folder("detected_frames")

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("output.avi", fourcc, 20.0, (1020, 500))
    frame_id = 0

    # --- Main Loop ---
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_id += 1
        frame = cv2.resize(frame, (1020, 500))

        detections = detector.detect(frame)
        tracked_objects = tracker.update(detections)

        for bbox in tracked_objects:
            x1, y1, x2, y2, object_id = bbox
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            speed_down = speed_estimator.calculate_speed(cy, object_id, "down")
            speed_up = speed_estimator.calculate_speed(cy, object_id, "up")

            speed = speed_down or speed_up
            draw_info(frame, speed, (x1, y1, x2, y2), object_id)

        draw_lines(frame, red_line_y, blue_line_y)
        save_frame(frame, "detected_frames", frame_id)
        out.write(frame)

        cv2.imshow("Vehicle Speed Detection", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break

    # --- Cleanup ---
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
