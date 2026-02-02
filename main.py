import cv2
import time

from detector.yolo_detector import YOLODetector
from behavior.motion import analyze_behavior, detect_and_track_unknowns
from narration.console_output import render_console, log_to_file


from attributes.size import estimate_size
from attributes.color import dominant_color
from attributes.distance import estimate_distance




# -------------------------
# Phase 3: Temporal memory
# -------------------------
object_history = {}
EXIT_THRESHOLD = 10  # frames


def main():
    cap = cv2.VideoCapture(0)
    detector = YOLODetector()

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return

    print("✅ Camera opened. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect_and_track(frame)

        # Phase 3 per-frame init
        current_ids = set()
        now = time.time()

        object_states = []

        # -------------------------
        # Known objects
        # -------------------------
        for det in detections:
            obj_id = det["id"]
            bbox = det["bbox"]
            x1, y1, x2, y2 = bbox

            current_ids.add(obj_id)

            # -------- Phase 3: history init/update --------
            if obj_id not in object_history:
                object_history[obj_id] = {
                    "first_seen": now,
                    "last_seen": now,
                    "last_bbox": bbox,
                    "frames_seen": 1
                }
                temporal_behavior = "entered_scene"
            else:
                prev_bbox = object_history[obj_id]["last_bbox"]
                object_history[obj_id]["last_seen"] = now
                object_history[obj_id]["frames_seen"] += 1

                prev_y = (prev_bbox[1] + prev_bbox[3]) / 2
                curr_y = (bbox[1] + bbox[3]) / 2

                if abs(curr_y - prev_y) < 5:
                    temporal_behavior = "stationary"
                elif curr_y < prev_y:
                    temporal_behavior = "moving up"
                else:
                    temporal_behavior = "moving down"

                object_history[obj_id]["last_bbox"] = bbox

            duration = round(
                object_history[obj_id]["last_seen"]
                - object_history[obj_id]["first_seen"],
                2
            )

            # -------- Phase 2: attributes --------
            size = estimate_size(bbox, frame.shape)
            obj_color = dominant_color(frame, bbox)
            distance = estimate_distance(bbox, frame.shape)

            # -------- Drawing --------
            draw_color = (0, 255, 0)
            conf = det["confidence"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), draw_color, 2)
            cv2.putText(
                frame,
                f"{det['class']} #{obj_id}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                draw_color,
                2
            )

            # -------- Store perception --------
            object_states.append({
                "id": obj_id,
                "object": det["class"],
                "size": size,
                "color": obj_color,
                "distance": distance,
                "motion": temporal_behavior,
                "confidence": round(conf, 2),
                "duration": duration,
                "description": (
                    f"{size} {obj_color} {det['class']} {distance}, "
                    f"{temporal_behavior} for {duration}s"
                )
            })

        # -------------------------
        # Unknown objects
        # -------------------------
        unknowns = detect_and_track_unknowns(frame, detections)

        for unk in unknowns:
            x, y, w, h = unk["bbox"]
            uid = unk["id"]
            draw_color = unk["color"]

            cv2.rectangle(frame, (x, y), (x + w, y + h), draw_color, 2)
            cv2.putText(
                frame,
                f"unknown #{uid}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                draw_color,
                2
            )

            object_states.append({
                "id": uid,
                "object": "unknown",
                "size": "unknown",
                "color": "unknown",
                "distance": "unknown",
                "motion": "moving",
                "confidence": "N/A",
                "duration": "N/A",
                "description": "unknown object moving"
            })

        # -------------------------
        # Phase 3: exit detection
        # -------------------------
        for oid in list(object_history.keys()):
            if oid not in current_ids:
                object_history[oid]["frames_seen"] -= 1
                if object_history[oid]["frames_seen"] < -EXIT_THRESHOLD:
                    del object_history[oid]

        # -------------------------
        # Output
        # -------------------------
        render_console(object_states)
        last_frame_objects = object_states.copy()
    

        cv2.imshow("SentioVision - Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
    if last_frame_objects:
        log_to_file(last_frame_objects)
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
