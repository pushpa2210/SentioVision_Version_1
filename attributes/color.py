import cv2
import numpy as np

def dominant_color(frame, bbox):
    x1, y1, x2, y2 = bbox
    roi = frame[y1:y2, x1:x2]
    if roi.size == 0:
        return "unknown"

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    hue = hsv[:, :, 0].mean()

    if hue < 10 or hue > 160:
        return "red"
    elif hue < 25:
        return "orange"
    elif hue < 35:
        return "yellow"
    elif hue < 85:
        return "green"
    elif hue < 125:
        return "blue"
    else:
        return "unknown"
