from ultralytics import YOLO
MIN_CONFIDENCE = 0.65
SMALL_OBJECT_AREA = 1500


class YOLODetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect_and_track(self, frame):
        results = self.model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False
        )

        detections = []

        for r in results:
            if r.boxes.id is None:
                continue

            for box, track_id in zip(r.boxes, r.boxes.id):
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = self.model.names[cls_id]
                area = (x2 - x1) * (y2 - y1)
                
                is_suspicious = False
                if conf < MIN_CONFIDENCE and area < SMALL_OBJECT_AREA:
                    is_suspicious = True



                detections.append({
                    "id": int(track_id),
                    "class": None if is_suspicious else label,
                    "bbox": [x1, y1, x2, y2],
                    "confidence": conf,
                    "suspicious": is_suspicious
                })
        return detections


