import cv2


def build_frame_index(tracks):
    frame_tracks = {}

    for track_id, items in tracks.items():
        for item in items:
            frame_idx = item["frame"]
            bbox = item["bbox"]

            if frame_idx not in frame_tracks:
                frame_tracks[frame_idx] = []

            frame_tracks[frame_idx].append({
                "track_id": track_id,
                "bbox": bbox
            })

    return frame_tracks

import cv2


def render_validation_video(video_path, output_path, frame_tracks, stationary_events):
    stationary_ids = {str(event["track_id"]) for event in stationary_events}
    stationary_meta = {
        str(event["track_id"]): event for event in stationary_events
    }

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        items = frame_tracks.get(frame_idx, [])

        for item in items:
            track_id = str(item["track_id"])
            x1, y1, x2, y2 = map(int, item["bbox"])

            if track_id in stationary_ids:
                color = (0, 0, 255)  # 紅色
                event = stationary_meta[track_id]
                text = (
                    f"ID {track_id} | STAY | "
                    f"{event['duration']}s"
                )
            else:
                color = (0, 255, 0)  # 綠色
                text = f"ID {track_id}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame,
                text,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )

        writer.write(frame)
        frame_idx += 1

    cap.release()
    writer.release()
