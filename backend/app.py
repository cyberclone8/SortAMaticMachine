import cv2
import time
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

# === Import your hardware control modules ===
from helpers.conveyor import MotorController  # from your L298N module
from helpers.servo import PCA9685Controller   # from your PCA9685 module
from helpers.camera import CameraStream
from utils.inference import detect_objects
from utils.class_mapping import classify_detection, CATEGORY_COLORS, CLASS_TO_CATEGORY

# === Initialize FastAPI ===
app = FastAPI()

# Global lock to ensure segregation runs one at a time
segregation_lock = asyncio.Lock()

# Allow your frontend to connect
origins = [
    "http://192.168.68.126:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Origins allowed
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, etc.
    allow_headers=["*"],          # All headers allowed
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
# Shared camera instance
camera = CameraStream(cam_index=0)
camera.start()

@app.get("/camera/mjpeg")
def camera_mjpeg():
    def mjpeg_generator():
        while True:
            frame = camera.get_frame()
            if frame is None:
                time.sleep(0.03)
                continue

            _, jpeg = cv2.imencode(".jpg", frame)
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n"
            )
            time.sleep(0.03)

    return StreamingResponse(
        mjpeg_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
        },
    )


# === WebSocket Endpoint for Realtime Inference ===
@app.websocket("/ws/inference")
async def ws_inference(ws: WebSocket):
    await ws.accept()
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

            frame = camera.get_frame()
            if frame is None:
                await asyncio.sleep(0.1)
                continue

            detections = detect_objects(frame)
            results = []
            for det in detections:
                cls = det["class"]
                conf = det["confidence"]
                category = classify_detection(cls)
                results.append({
                    "detected_class": cls,
                    "confidence": conf,
                    "category": category,
                })

            await ws.send_json({"detections": results})
            await asyncio.sleep(0.2)
    except WebSocketDisconnect:
        print("[INFO] WebSocket disconnected")
    finally:
        command_task.cancel()

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
        "biodegradable": {
            "channel": 0,   # first servo
            "angle": 0,     # rotate to 0 degrees
            "duration": 4   # run conveyor for 4 seconds
        },
        "non_biodegradable": {
            "channel": 0,   # same servo as biodegradable
            "angle": 180,   # rotate to 180 degrees
            "duration": 3   # run conveyor for 3 seconds
        },
        "recyclable": {
            "channel": 1,   # second servo
            "angle": 0,     # rotate to 0 degrees
            "duration": 2   # run conveyor for 2 seconds
        },
        "paper": {
            "channel": 1,   # same second servo
            "angle": 180,   # rotate to 180 degrees
            "duration": 1   # run conveyor for 1 second
        }
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
    print("[INFO] Stopping camera stream...")
    camera.stop()

# === Run the API ===
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
