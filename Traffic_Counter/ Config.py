# config.py
"""
Configuration file for Traffic Vehicle Counter Project
"""

# Google Drive
FILE_ID = "1RLmqoMl0WTtng_vhvWt-ATHrGqzjtgr6" # Id of the video for analysis
DEST_PATH = "./data/Vancouver_Traffic_Intersection.MP4" # link to the video

# YOLO Model
MODEL_PATH = "./models/yolov9c.pt"
CLASSES_TO_TRACK = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 
'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 
'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 
'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard']

# Line coordinates
LINE_COORDS = {
    "nb": {"start": (880, 390), "end": (1000, 380), "label": "NB Incoming"},
    "sb": {"start": (740, 660), "end": (1010, 620), "label": "SB Incoming"},
    "wb": {"start": (630, 430), "end": (630, 620), "label": "WB Incoming"},
}
