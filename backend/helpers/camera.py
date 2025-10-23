import cv2
import asyncio
import threading
from queue import Queue

class CameraStream:
    def __init__(self, cam_index=0):
        self.cam_index = cam_index
        self.cap = None
        self.frame = None
        self.running = False
        self.lock = threading.Lock()
        self.thread = None

    def start(self):
        """Start the camera capture in a background thread."""
        if self.running:
            return
        self.cap = cv2.VideoCapture(self.cam_index)
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera index {self.cam_index}")
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def _capture_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                # Try to recover after short delay
                self.cap.release()
                self.cap = cv2.VideoCapture(self.cam_index)
                continue
            with self.lock:
                self.frame = frame
        if self.cap:
            self.cap.release()

    def get_frame(self):
        """Return the latest frame."""
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        """Stop capturing."""
        self.running = False
        if self.thread:
            self.thread.join()
