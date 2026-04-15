from core.io_utils import load_json
from core.render import build_frame_index, render_validation_video
from config import *

def main():
    tracks = load_json(TRACKS_PATH)
    stationary_events = load_json(EVENTS_PATH)

    frame_tracks = build_frame_index(tracks)

    render_validation_video(
        video_path=VIDEO_PATH,
        output_path="outputs/validation_output.mp4",
        frame_tracks=frame_tracks,
        stationary_events=stationary_events
    )


if __name__ == "__main__":
    main()