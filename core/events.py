def count_labels(analyze_result):
    label_count = {}
    static_ids = []

    for track_id, result in analyze_result.items():
        label = result["label"]
        label_count[label] = label_count.get(label, 0) + 1

        if label == "static":
            static_ids.append(track_id)

    return {
        "label_count": label_count,
        "static_ids": static_ids,
    }


def find_stationary_tracks(
    analyze_result,
    min_duration=3.0,
    max_speed=10.0,
    max_distance=50.0,
):
    stationary_tracks = {}

    for track_id, result in analyze_result.items():
        if (
            result["duration"] >= min_duration
            and result["avg_speed_pixels_per_second"] <= max_speed
            and result["total_distance"] <= max_distance
        ):
            stationary_tracks[track_id] = result

    return stationary_tracks


def export_stationary_events(stationary_tracks):
    events = []

    for track_id, result in sorted(stationary_tracks.items(), key=lambda x: int(x[0])):
        events.append({
            "track_id": track_id,
            "event": "person_staying",
            "start_frame": result["start_frame"],
            "end_frame": result["end_frame"],
            "duration": round(result["duration"], 2),
            "avg_speed_pixels_per_second": round(result["avg_speed_pixels_per_second"], 2),
            "total_distance": round(result["total_distance"], 2),
        })

    return events


def print_stationary_tracks(stationary_tracks):
    for track_id, result in sorted(stationary_tracks.items(), key=lambda x: int(x[0])):
        print(
            track_id,
            "duration =", round(result["duration"], 2),
            "speed =", round(result["avg_speed_pixels_per_second"], 2),
            "distance =", round(result["total_distance"], 2),
            "movement_time =", round(result["movement_time"], 2),
        )
