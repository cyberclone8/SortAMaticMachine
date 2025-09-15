import cv2, time, asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

# from helpers.pca9685_servo import PCA9685ServoController
from config import get_servo_gpio_config
from helpers.servo_pigpio import GPIOServoController
from helpers.l298n_motor import L298NConveyor
from helpers.loadcells import MultiLoadCell
from utils.inference import detect_objects
from utils.class_mapping import classify_detection, CATEGORY_COLORS, CLASS_TO_CATEGORY

app = FastAPI()

# ✅ Allow requests from your frontend
origins = [
    "http://localhost:5173",  # React dev server
    # "http://your-frontend-domain.com",  # Production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # can also use ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],     # allow all HTTP methods
    allow_headers=["*"],     # allow all headers
)



# Configuration
SERVO_CHANNEL_MAP = {
    'biodegradable': 0,
    'non_biodegradable': 1,
    'recyclable': 2,
    'paper': 3,
    'spare': 4,
}

SERVO_MOVE_US = {
    'biodegradable': 1200,
    'non_biodegradable': 1800,
    'recyclable': 1400,
    'paper': 1600,
    'spare': 1500,
}

SERVO_MOVE_TIME = {
    'biodegradable': 0.5,
    'non_biodegradable': 1.0,
    'recyclable': 0.7,
    'paper': 0.4,
    'spare': 0.3,
}

# servo_ctrl = PCA9685ServoController()
servo_cfg = get_servo_gpio_config()
servo_ctrl = GPIOServoController(servo_cfg)
conveyor = L298NConveyor(en_pin=18, in1_pin=23, in2_pin=24)

loadcells = MultiLoadCell([
    {'name': 'loadcell1', 'dout_pin': 5, 'pd_sck_pin': 6},
    {'name': 'loadcell2', 'dout_pin': 13, 'pd_sck_pin': 6},
    {'name': 'loadcell3', 'dout_pin': 19, 'pd_sck_pin': 6},
    {'name': 'loadcell4', 'dout_pin': 26, 'pd_sck_pin': 6},
])

CAM_INDEX = 0

def mjpeg_generator():
    cap = cv2.VideoCapture(CAM_INDEX)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            detections = detect_objects(frame)
            for i, det in enumerate(detections):
                x1, y1, x2, y2 = det['bbox']
                cls = det['class']
                conf = det['confidence']
                category = classify_detection(cls)
                color = CATEGORY_COLORS.get(category, (255,255,255))
                # draw box and label
                cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
                cv2.putText(frame, f"{cls} ({category}) {conf:.2f}", (x1, max(10,y1-10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            _, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.03)
    finally:
        cap.release()

@app.get('/camera/mjpeg')
def camera_mjpeg():
    return StreamingResponse(mjpeg_generator(), media_type='multipart/x-mixed-replace; boundary=frame',  headers={
            "Access-Control-Allow-Origin": "*",  # allow frontend to use the feed in canvas
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
        })

@app.websocket('/ws/inference')
async def ws_inference(ws: WebSocket):
    await ws.accept()
    cap = cv2.VideoCapture(CAM_INDEX)
    paused = False  # backend pause flag

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
            pass  # ignore if connection closed

    # Run command receiver in background
    command_task = asyncio.create_task(receive_commands())

    try:
        while True:
            if paused:
                await asyncio.sleep(0.1)  # skip processing while paused
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

                # Send all detections for this frame
                await ws.send_json({'detections': results})
            else:
                await ws.send_json({'detections': []})

            await asyncio.sleep(0.2)

    except WebSocketDisconnect:
        pass
    finally:
        command_task.cancel()  # stop receiving commands
        cap.release()

@app.get('/loadcells/weights')
def get_all_weights():
    return JSONResponse(loadcells.get_all_weights())

@app.post('/conveyor/set_speed')
def conveyor_set_speed(speed: float):
    conveyor.set_speed(speed)
    return JSONResponse({'status': 'ok', 'speed': speed})

@app.post('/conveyor/stop')
def conveyor_stop():
    conveyor.stop()
    return JSONResponse({'status': 'stopped'})

@app.post('/conveyor/start')
def conveyor_start(speed: float = 50.0):
    """
    Start the conveyor at a default or given speed (percentage 0-100).
    """
    conveyor.set_speed(speed)
    return JSONResponse({'status': 'started', 'speed': speed})

@app.post('/servo/move')
def move_servo(category: str, angle: float = None, microseconds: int = None):
    servo_ctrl.move_servo(category, angle=angle, microseconds=microseconds)
    return JSONResponse({'status': 'moved', 'category': category})

@app.post("/segregate")
def segregate(data: dict):
    if "category" in data and "detected_class" in data:
        category = data["category"]
        detected_class = data["detected_class"]

        # Conveyor + servo timing from tables
        dur = SERVO_MOVE_TIME.get(category, 0.5)
        micros = SERVO_MOVE_US.get(category, 1500)

        # Step 1: Move conveyor
        conveyor.set_speed(60.0)
        time.sleep(dur)
        conveyor.stop()

        # Step 2: Move corresponding servo
        servo_ctrl.move_servo(category, microseconds=micros)
        time.sleep(0.5)  # let servo actuate
        servo_ctrl.move_servo(category, microseconds=1500)  # back to neutral

        return JSONResponse({
            "status": "completed",
            "classification": category,
            "object": detected_class
        })

    return JSONResponse(
        {"status": "failed", "reason": "Missing fields"},
        status_code=400
    )
    


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
