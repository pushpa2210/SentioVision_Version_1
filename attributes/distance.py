def estimate_distance(bbox, frame_shape):
    x1, y1, x2, y2 = bbox
    box_height = y2 - y1
    frame_height = frame_shape[0]
    ratio = box_height / frame_height

    if ratio > 0.6:
        return "near"
    elif ratio > 0.3:
        return "mid"
    else:
        return "far"
