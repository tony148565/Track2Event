import math


def bbox_center(bbox):
    x1, y1, x2, y2 = bbox
    return [(x1 + x2) / 2.0, (y1 + y2) / 2.0]


def classify_motion(avg_speed, duration):
    if duration < 1.0:
        return "noise"
    if avg_speed < 20:
        return "static"
    if avg_speed < 80:
        return "walking"
    return "fast_moving"


def compute_track_speed(track_data, fps=23.98, max_frame_gap=5, max_speed=300.0):
    if len(track_data) < 2:
        return {
            "avg_speed_pixels_per_second": 0.0,
            "total_distance": 0.0,
            "movement_time": 0.0,
            "duration": 0.0,
            "valid_segments": 0,
            "label": "noise",
        }

    track_data = sorted(track_data, key=lambda x: x["frame"])

    total_distance = 0.0
    total_time = 0.0
    valid_segments = 0

    for i in range(1, len(track_data)):
        prev_item = track_data[i - 1]
        curr_item = track_data[i]

        frame_gap = curr_item["frame"] - prev_item["frame"]
        if frame_gap <= 0 or frame_gap > max_frame_gap:
            continue

        prev_center = bbox_center(prev_item["bbox"])
        curr_center = bbox_center(curr_item["bbox"])

        dx = curr_center[0] - prev_center[0]
        dy = curr_center[1] - prev_center[1]
        distance = math.sqrt(dx * dx + dy * dy)

        time_gap = frame_gap / fps
        total_distance += distance
        total_time += time_gap
        valid_segments += 1

    if total_time <= 0 or valid_segments == 0:
        return {
            "avg_speed_pixels_per_second": 0.0,
            "total_distance": 0.0,
            "movement_time": 0.0,
            "duration": 0.0,
            "valid_segments": 0,
            "label": "noise",
        }

    avg_speed = min(total_distance / total_time, max_speed)

    start_frame = track_data[0]["frame"]
    end_frame = track_data[-1]["frame"]
    duration = (end_frame - start_frame) / fps
    label = classify_motion(avg_speed, duration)

    return {
        "start_frame": int(start_frame),
        "end_frame": int(end_frame),
        "avg_speed_pixels_per_second": float(avg_speed),
        "total_distance": float(total_distance),
        "movement_time": float(total_time),
        "duration": float(duration),
        "valid_segments": int(valid_segments),
        "label": label,
    }


def analyze_tracks_speed(
    tracks,
    fps=23.98,
    min_track_points=5,
    max_frame_gap=5,
    max_speed=300.0,
):
    analyze_result = {}

    for track_id, data in tracks.items():
        if len(data) < min_track_points:
            continue

        result = compute_track_speed(
            data,
            fps=fps,
            max_frame_gap=max_frame_gap,
            max_speed=max_speed,
        )

        if result["valid_segments"] == 0:
            continue

        analyze_result[track_id] = result

    return analyze_result