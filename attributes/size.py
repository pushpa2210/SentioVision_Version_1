def estimate_size(bbox, frame_shape):
    x1, y1, x2, y2 = bbox
    box_area = (x2 - x1) * (y2 - y1)
    frame_area = frame_shape[0] * frame_shape[1]
    ratio = box_area / frame_area

    if ratio < 0.01:
        return "small"
    elif ratio < 0.05:
        return "medium"
    else:
        return "large"
