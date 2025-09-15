import cv2
from ultralytics import YOLO

# Load YOLOv8 pretrained model (nano version is fastest)
model = YOLO("yolov8n.pt")

def run_camera_test(cam_index=0, conf=0.25):
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print(f"❌ Could not open camera index {cam_index}")
        return

    print("✅ Camera opened. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame from camera")
            break

        # Run YOLO inference
        results = model.predict(source=frame, conf=conf, verbose=False)

        # Draw results on frame
        annotated = results[0].plot()

        # Show frame
        cv2.imshow("YOLOv8 Live Camera", annotated)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Change cam_index to 1 if you're using an external USB cam
    run_camera_test(cam_index=0, conf=0.25)