# Full mapping of YOLOv8 COCO-80 classes into 5 categories:
# biodegradable, non_biodegradable, recyclable, paper, spare

COCO_CLASSES = [
    'person','bicycle','car','motorcycle','airplane','bus','train','truck','boat','traffic light',
    'fire hydrant','stop sign','parking meter','bench','bird','cat','dog','horse','sheep','cow',
    'elephant','bear','zebra','giraffe','backpack','umbrella','handbag','tie','suitcase','frisbee',
    'skis','snowboard','sports ball','kite','baseball bat','baseball glove','skateboard','surfboard','tennis racket',
    'bottle','wine glass','cup','fork','knife','spoon','bowl','banana','apple','sandwich','orange',
    'broccoli','carrot','hot dog','pizza','donut','cake','chair','couch','potted plant','bed',
    'dining table','toilet','tv','laptop','mouse','remote','keyboard','cell phone','microwave','oven',
    'toaster','sink','refrigerator','book','clock','vase','scissors','teddy bear','hair drier','toothbrush'
]

# A pragmatic mapping — tweak according to your actual waste definitions.
CLASS_TO_CATEGORY = {
    # Biodegradable: foods and organic waste
    'banana': 'biodegradable', 'apple': 'biodegradable', 'sandwich': 'biodegradable',
    'orange': 'biodegradable', 'broccoli': 'biodegradable', 'carrot': 'biodegradable',
    'hot dog': 'biodegradable', 'pizza': 'biodegradable', 'donut': 'biodegradable',
    'cake': 'biodegradable',

    # Recyclable: typical recyclables (glass, plastic containers, metal-like utensils)
    'bottle': 'recyclable', 'wine glass': 'recyclable', 'cup': 'recyclable',
    'bowl': 'recyclable', 'vase': 'recyclable', 'fork': 'recyclable',
    'knife': 'recyclable', 'spoon': 'recyclable',

    # Paper: paper-like items
    'book': 'paper',

    # Non-biodegradable: electronics, furniture, vehicles, many household items
    'person': 'non_biodegradable', 'bicycle': 'non_biodegradable', 'car': 'non_biodegradable',
    'motorcycle': 'non_biodegradable', 'airplane': 'non_biodegradable', 'bus': 'non_biodegradable',
    'train': 'non_biodegradable', 'truck': 'non_biodegradable', 'boat': 'non_biodegradable',
    'traffic light': 'non_biodegradable', 'fire hydrant': 'non_biodegradable', 'stop sign': 'non_biodegradable',
    'parking meter': 'non_biodegradable', 'bench': 'non_biodegradable', 'bird': 'non_biodegradable',
    'cat': 'non_biodegradable', 'dog': 'non_biodegradable', 'horse': 'non_biodegradable',
    'sheep': 'non_biodegradable', 'cow': 'non_biodegradable', 'elephant': 'non_biodegradable',
    'bear': 'non_biodegradable', 'zebra': 'non_biodegradable', 'giraffe': 'non_biodegradable',
    'backpack': 'non_biodegradable', 'umbrella': 'non_biodegradable', 'handbag': 'non_biodegradable',
    'tie': 'non_biodegradable', 'suitcase': 'non_biodegradable', 'frisbee': 'non_biodegradable',
    'skis': 'non_biodegradable', 'snowboard': 'non_biodegradable', 'sports ball': 'non_biodegradable',
    'kite': 'non_biodegradable', 'baseball bat': 'non_biodegradable', 'baseball glove': 'non_biodegradable',
    'skateboard': 'non_biodegradable', 'surfboard': 'non_biodegradable', 'tennis racket': 'non_biodegradable',
    'banana': 'biodegradable', 'chair': 'non_biodegradable', 'couch': 'non_biodegradable',
    'potted plant': 'non_biodegradable', 'bed': 'non_biodegradable', 'dining table': 'non_biodegradable',
    'toilet': 'non_biodegradable', 'tv': 'non_biodegradable', 'laptop': 'non_biodegradable',
    'mouse': 'non_biodegradable', 'remote': 'non_biodegradable', 'keyboard': 'non_biodegradable',
    'cell phone': 'non_biodegradable', 'microwave': 'non_biodegradable', 'oven': 'non_biodegradable',
    'toaster': 'non_biodegradable', 'sink': 'non_biodegradable', 'refrigerator': 'non_biodegradable',
    'clock': 'non_biodegradable', 'scissors': 'non_biodegradable', 'teddy bear': 'non_biodegradable',
    'hair drier': 'non_biodegradable', 'toothbrush': 'non_biodegradable'
}

# Ensure every COCO class has a mapping; default to 'spare'
for cls in COCO_CLASSES:
    if cls not in CLASS_TO_CATEGORY:
        CLASS_TO_CATEGORY[cls] = 'spare'

CATEGORY_COLORS = {
    'biodegradable': (0, 255, 0),
    'non_biodegradable': (0, 0, 255),
    'recyclable': (0, 165, 255),
    'paper': (0, 255, 255),
    'spare': (128, 128, 128)
}

def classify_detection(det_class: str) -> str:
    return CLASS_TO_CATEGORY.get(det_class, 'spare')
