import os
import torch

from core.io_utils import load_json, save_json
from core.tracking import build_model, build_tracks
from core.features import analyze_tracks_speed
from core.events import (
    count_labels,
    find_stationary_tracks,
    export_stationary_events,
    print_stationary_tracks,
)
from config import *


def main():
    print("cuda available:", torch.cuda.is_available())

    model = build_model(MODEL_PATH)

    if os.path.exists(TRACKS_PATH):
        tracks = load_json(TRACKS_PATH)
    else:
        tracks = build_tracks(model, source=VIDEO_PATH, tracker="bytetrack.yaml")
        save_json(tracks, TRACKS_PATH)

    print("track count:", len(tracks))

    analyze_result = analyze_tracks_speed(
        tracks,
        fps=23.98,
        min_track_points=5,
        max_frame_gap=5,
        max_speed=300.0,
    )
    save_json(analyze_result, ANALYZE_PATH)

    print("analyzed track count:", len(analyze_result))

    stats = count_labels(analyze_result)
    print("label count:", stats["label_count"])
    print("static ids:", stats["static_ids"])

    stationary_tracks = find_stationary_tracks(
        analyze_result,
        min_duration=3.0,
        max_speed=10.0,
        max_distance=50.0,
    )
    print("stationary track count:", len(stationary_tracks))
    print_stationary_tracks(stationary_tracks)

    stationary_events = export_stationary_events(stationary_tracks)
    save_json(stationary_events, EVENTS_PATH)

    print("stationary events count:", len(stationary_events))


if __name__ == "__main__":
    main()