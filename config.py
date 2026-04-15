# config.py
import os

MODEL_PATH = os.getenv("VIDEO_ANALYSIS_MODEL_PATH", "models/yolov8x.pt")
VIDEO_PATH = os.getenv("VIDEO_PATH", "data/video.mp4")

TRACKS_PATH = "outputs/tracks.json"
ANALYZE_PATH = "outputs/analyze_result.json"
EVENTS_PATH = "outputs/stationary_events.json"


FPS = 23.98

MIN_TRACK_POINTS = 5
MAX_FRAME_GAP = 5
MAX_SPEED = 300.0

STATIONARY_MIN_DURATION = 3.0
STATIONARY_MAX_SPEED = 10.0
STATIONARY_MAX_DISTANCE = 50.0