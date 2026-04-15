import argparse
from core.pipeline import run_track2event


def parse_args():
    parser = argparse.ArgumentParser(description="Track2Event CLI")
    parser.add_argument("--video", default=None, help="Path to input video")
    parser.add_argument("--model", default=None, help="Path to YOLO model")
    parser.add_argument("--tracks", default=None, help="Path to tracks.json")
    parser.add_argument("--analyze", default=None, help="Path to analyze_result.json")
    parser.add_argument("--events", default=None, help="Path to stationary_events.json")
    return parser.parse_args()


def main():
    args = parse_args()

    kwargs = {}
    if args.video is not None:
        kwargs["video_path"] = args.video
    if args.model is not None:
        kwargs["model_path"] = args.model
    if args.tracks is not None:
        kwargs["tracks_path"] = args.tracks
    if args.analyze is not None:
        kwargs["analyze_path"] = args.analyze
    if args.events is not None:
        kwargs["events_path"] = args.events

    result = run_track2event(**kwargs)

    print("done")
    print("tracks:", len(result["tracks"]))
    print("analyze_result:", len(result["analyze_result"]))
    print("stationary_events:", len(result["stationary_events"]))


if __name__ == "__main__":
    main()