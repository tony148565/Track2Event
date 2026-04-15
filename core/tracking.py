from ultralytics import YOLO


def build_model(model_path):
    return YOLO(model_path)


def build_tracks(model, source="video.mp4", tracker="bytetrack.yaml", target_class=0):
    tracks = {}

    results = model.track(
        source=source,
        tracker=tracker
    )

    for frame_idx, r in enumerate(results):
        boxes = r.boxes

        if boxes.id is None or boxes.cls is None:
            continue

        ids = boxes.id.cpu().numpy()
        xyxy = boxes.xyxy.cpu().numpy()
        clss = boxes.cls.cpu().numpy()

        for i, track_id in enumerate(ids):
            class_id = int(clss[i])

            if class_id != target_class:
                continue

            track_id = str(int(track_id))
            bbox = xyxy[i].tolist()

            if track_id not in tracks:
                tracks[track_id] = []

            tracks[track_id].append({
                "frame": int(frame_idx),
                "bbox": [float(v) for v in bbox]
            })

    return tracks