import cv2
try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except Exception:
    ULTRALYTICS_AVAILABLE = False

model = None
if ULTRALYTICS_AVAILABLE:
    try:
        model = YOLO('yolov8n.pt')
    except Exception as e:
        print(f"[WARN] Could not load YOLO model: {e}")
        model = None
else:
    print('[SIM] ultralytics not available — running detection simulation')

def detect_objects(frame):
    """Return list of detections with keys: class, confidence, bbox (x1,y1,x2,y2)
    If model not available, returns empty list (simulation).
    """
    if model is None:
        # Simulation: return empty list (or you can simulate a fake detection)
        return []
    # ultralytics supports passing numpy array directly
    results = model.predict(source=frame, conf=0.5, verbose=False)
    # results = model(frame, conf=0.1, verbose=False)
    detections = []
    for r in results:
        # r.boxes is tensor-like; iterate
        boxes = getattr(r, 'boxes', None)
        if boxes is None:
            continue
        for box in boxes:
            try:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].cpu().numpy() if hasattr(box.xyxy[0], 'cpu') else box.xyxy[0]
                x1, y1, x2, y2 = map(int, xyxy)
                label = model.names[cls_id]
                detections.append({
                    'class': label,
                    'confidence': conf,
                    'bbox': (x1, y1, x2, y2)
                })
            except Exception:
                continue
    return detections
