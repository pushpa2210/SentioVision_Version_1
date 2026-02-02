import math

# Store previous positions for each tracked ID
track_history = {}

def analyze_behavior(track_id, bbox):
    """
    track_id: int
    bbox: [x1, y1, x2, y2]
    returns: behavior string
    """

    x1, y1, x2, y2 = bbox
    cx = int((x1 + x2) / 2)
    cy = int((y1 + y2) / 2)

    if track_id not in track_history:
        track_history[track_id] = (cx, cy)
        return "stationary"

    prev_cx, prev_cy = track_history[track_id]

    dx = cx - prev_cx
    dy = cy - prev_cy

    distance = math.sqrt(dx*dx + dy*dy)

    track_history[track_id] = (cx, cy)

    if distance < 5:
        return "stationary"

    if abs(dx) > abs(dy):
        return "moving right" if dx > 0 else "moving left"
    else:
        return "moving down" if dy > 0 else "moving up"


#unknown object motion detection
import cv2
import numpy as np
import math
import random

# --- UNKNOWN OBJECT TRACKING STATE ---
prev_gray = None
unknown_tracks = {}
unknown_id_counter = 1
unknown_colors = {}

def get_color_for_id(track_id):
    if track_id not in unknown_colors:
        unknown_colors[track_id] = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
    return unknown_colors[track_id]


def detect_and_track_unknowns(frame, detections):
    """
    frame: current BGR frame
    detections: YOLO detections (known objects)
    returns: list of unknown objects with id, bbox, color
    """

    global prev_gray, unknown_id_counter

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_gray is None:
        prev_gray = gray
        return []

    diff = cv2.absdiff(prev_gray, gray)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    prev_gray = gray
    results = []

    for cnt in contours:
        if cv2.contourArea(cnt) < 800:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        # Check overlap with known detections
        overlaps_known = False
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            if x < x2 and x + w > x1 and y < y2 and y + h > y1:
                overlaps_known = True
                break

        if overlaps_known:
            continue

        cx = x + w // 2
        cy = y + h // 2

        matched_id = None
        for uid, (px, py) in unknown_tracks.items():
            if math.hypot(cx - px, cy - py) < 50:
                matched_id = uid
                break

        if matched_id is None:
            matched_id = unknown_id_counter
            unknown_tracks[matched_id] = (cx, cy)
            unknown_id_counter += 1
        else:
            unknown_tracks[matched_id] = (cx, cy)

        color = get_color_for_id(matched_id)

        results.append({
            "id": matched_id,
            "bbox": (x, y, w, h),
            "color": color
        })

    return results

