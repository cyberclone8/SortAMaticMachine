import cv2
import time
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

# === Import your hardware control modules ===
from helpers.conveyor import MotorController  # from your L298N module
from helpers.servo import PCA9685Controller   # from your PCA9685 module
from utils.inference import detect_objects
from utils.class_mapping import classify_detection, CATEGORY_COLORS, CLASS_TO_CATEGORY

# === Initialize FastAPI ===
app = FastAPI()

# Global lock to ensure segregation runs one at a time
segregation_lock = asyncio.Lock()

# Allow your frontend to connect
origins = ["http://localhost:5173"]  # Add your production domain here if needed

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Configuration ===
SERVO_CHANNEL_MAP = {
    'biodegradable': 0,
    'non_biodegradable': 1,
    'recyclable': 2,
    'paper': 3,
    'spare': 4,
}

SERVO_MOVE_TIME = {
    'biodegradable': 0.5,
    'non_biodegradable': 1.0,
    'recyclable': 0.7,
    'paper': 0.4,
    'spare': 0.3,
}

# === Initialize hardware controllers ===
servo_ctrl = PCA9685Controller()  # Uses I2C bus 3, addr 0x40 by default
conveyor = MotorController(en_pin=25, in1_pin=24, in2_pin=23)

CAM_INDEX = 0  # Camera device index

# === MJPEG Camera Stream ===
def mjpeg_generator():
    cap = cv2.VideoCapture(CAM_INDEX)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            detections = detect_objects(frame)
            for det in detections:
                x1, y1, x2, y2 = det['bbox']
                cls = det['class']
                conf = det['confidence']
                category = classify_detection(cls)
                color = CATEGORY_COLORS.get(category, (255, 255, 255))
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(
                    frame,
                    f"{cls} ({category}) {conf:.2f}",
                    (x1, max(10, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2,
                )

            _, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n'
            )
            time.sleep(0.03)
    finally:
        cap.release()


@app.get('/camera/mjpeg')
def camera_mjpeg():
    return StreamingResponse(
        mjpeg_generator(),
        media_type='multipart/x-mixed-replace; boundary=frame',
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
        },
    )


# === WebSocket Endpoint for Realtime Inference ===
@app.websocket('/ws/inference')
async def ws_inference(ws: WebSocket):
    await ws.accept()
    cap = cv2.VideoCapture(CAM_INDEX)
    paused = False

    async def receive_commands():
        nonlocal paused
        try:
            while True:
                msg = await ws.receive_text()
                if msg.lower() == "pause":
                    paused = True
                elif msg.lower() == "resume":
                    paused = False
        except Exception:
            pass  # WebSocket closed

    command_task = asyncio.create_task(receive_commands())

    try:
        while True:
            if paused:
                await asyncio.sleep(0.1)
                continue

            ret, frame = cap.read()
            if not ret:
                await ws.send_json({'error': 'camera_read_failed'})
                break

            detections = detect_objects(frame)
            if detections:
                results = []
                for det in detections:
                    cls = det['class']
                    conf = det['confidence']
                    category = classify_detection(cls)
                    results.append({
                        'detected_class': cls,
                        'confidence': conf,
                        'category': category
                    })
                await ws.send_json({'detections': results})
            else:
                await ws.send_json({'detections': []})

            await asyncio.sleep(0.2)
    except WebSocketDisconnect:
        pass
    finally:
        command_task.cancel()
        cap.release()


# === Conveyor Control Endpoints ===
@app.post('/conveyor/set_speed')
def conveyor_set_speed(speed: float):
    conveyor.set_speed(speed)
    return JSONResponse({'status': 'ok', 'speed': speed})


@app.post('/conveyor/start')
def conveyor_start(speed: float = 50.0):
    conveyor.set_speed(speed)
    return JSONResponse({'status': 'started', 'speed': speed})


@app.post('/conveyor/stop')
def conveyor_stop():
    conveyor.stop()
    return JSONResponse({'status': 'stopped'})


# === Servo Control Endpoints ===
@app.post('/servo/move')
def move_servo(category: str, angle: float = None):
    """
    Move a servo based on category mapping and desired angle (0–180).
    """
    if category not in SERVO_CHANNEL_MAP:
        return JSONResponse({'error': 'invalid category'}, status_code=400)

    channel = SERVO_CHANNEL_MAP[category]

    if angle is not None:
        servo_ctrl.move_servo(channel, angle)
    else:
        # default center
        servo_ctrl.move_to_90(channel)

    return JSONResponse({'status': 'moved', 'category': category, 'angle': angle})


# === Segregation Endpoint ===
@app.post("/segregate")
async def segregate(data: dict):
    if "category" not in data:
        return JSONResponse(
            {"status": "failed", "reason": "Missing 'category' field"},
            status_code=400
        )

    category = data["category"].lower()
    servo_actions = {
        "biodegradable": {"channel": 1, "angle": 0, "duration": 4},
        "non_biodegradable": {"channel": 1, "angle": 180, "duration": 3},
        "recyclable": {"channel": 2, "angle": 0, "duration": 2},
        "paper": {"channel": 2, "angle": 180, "duration": 1},
    }

    if category not in servo_actions:
        return JSONResponse(
            {"status": "failed", "reason": f"Unknown category '{category}'"},
            status_code=400
        )

    action = servo_actions[category]

    async def run_segregation():
        async with segregation_lock:  # ensures only one segregation runs at a time
            try:
                # Step 1: Move conveyor at full speed (100%)
                print(f"[INFO] Starting segregation for '{category}' - full speed conveyor")
                conveyor.set_speed(100.0)
                await asyncio.sleep(action["duration"])
                conveyor.stop()
                print(f"[INFO] Conveyor stopped after {action['duration']}s")

                # Step 2: Move servo for category
                print(f"[INFO] Moving servo {action['channel']} to {action['angle']}°")
                servo_ctrl.move_servo(action["channel"], angle=action["angle"])
                await asyncio.sleep(0.5)

                # Step 3: Return servo to neutral position
                print(f"[INFO] Returning servo {action['channel']} to neutral (90°)")
                servo_ctrl.move_servo(action["channel"], angle=90)

                print(f"[✅ Completed segregation for '{category}']")

            except Exception as e:
                print(f"[⚠️ Segregation error] {e}")

    # Run the segregation logic in background
    asyncio.create_task(run_segregation())

    # Respond immediately
    return JSONResponse({
        "status": "processing",
        "message": f"Segregation started for '{category}' at full speed",
        "servo_channel": action["channel"],
        "target_angle": action["angle"],
        "conveyor_duration": action["duration"]
    })

@app.on_event("shutdown")
def shutdown_event():
    servo_ctrl.stop_all()
    conveyor.cleanup()
    print("Hardware safely shut down.")

# === Run the API ===
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
