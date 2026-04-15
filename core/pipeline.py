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


def run_track2event(
    video_path=VIDEO_PATH,
    model_path=MODEL_PATH,
    tracks_path=TRACKS_PATH,
    analyze_path=ANALYZE_PATH,
    events_path=EVENTS_PATH,
    fps=23.98,
    min_track_points=5,
    max_frame_gap=5,
    max_speed=300.0,
    min_duration=3.0,
    stationary_max_speed=10.0,
    stationary_max_distance=50.0,
    verbose=True
):
    if verbose:
        print("cuda available:", torch.cuda.is_available())

    model = build_model(model_path)

    if os.path.exists(tracks_path):
        tracks = load_json(tracks_path)
    else:
        tracks = build_tracks(model, source=video_path, tracker="bytetrack.yaml")
        save_json(tracks, tracks_path)
    
    if verbose:
        print("track count:", len(tracks))

    analyze_result = analyze_tracks_speed(
        tracks,
        fps=fps,
        min_track_points=min_track_points,
        max_frame_gap=max_frame_gap,
        max_speed=max_speed,
    )
    save_json(analyze_result, analyze_path)
    
    if verbose:
        print("analyzed track count:", len(analyze_result))
        stats = count_labels(analyze_result)
        print("label count:", stats["label_count"])
        print("static ids:", stats["static_ids"])

    stationary_tracks = find_stationary_tracks(
        analyze_result,
        min_duration=min_duration,
        max_speed=stationary_max_speed,
        max_distance=stationary_max_distance,
    )
    if verbose:
        print("stationary track count:", len(stationary_tracks))
        print_stationary_tracks(stationary_tracks)

    stationary_events = export_stationary_events(stationary_tracks)
    save_json(stationary_events, events_path)
    
    if verbose:
        print("stationary events count:", len(stationary_events))

    return {
        "tracks": tracks,
        "analyze_result": analyze_result,
        "stationary_events": stationary_events,
    }