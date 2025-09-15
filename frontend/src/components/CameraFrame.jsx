import React, { useState, useEffect, useRef } from "react";
import { createSocket } from "../utils/createSocket";
import { sendDetection } from "../utils/sendDetection";

const CameraFrame = ({ onDetection }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [paused, setPaused] = useState(false);
  const [snapshot, setSnapshot] = useState(null);

  const imgRef = useRef(null);
  const canvasRef = useRef(null);
  const latestDetection = useRef(null);
  const pauseTimer = useRef(null);
  const isPaused = useRef(false);
  const wsRef = useRef(null);

  const takeSnapshot = () => {
    const img = imgRef.current;
    const canvas = canvasRef.current;
    if (!img || !canvas) return null;

    const ctx = canvas.getContext("2d");
    canvas.width = img.naturalWidth || img.width;
    canvas.height = img.naturalHeight || img.height;
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

    return canvas.toDataURL("image/jpeg");
  };

  useEffect(() => {
    const ws = createSocket("ws://localhost:8000/ws/inference");
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("✅ WebSocket connected to /ws/inference");
      setLoading(false);
    };

    ws.onmessage = async (event) => {
      if (isPaused.current) return; // ignore all while paused

      try {
        const data = JSON.parse(event.data);

        if (data.error) {
          setError(data.error);
          latestDetection.current = null;
          return;
        }

        if (data.detections && data.detections.length > 0) {
          const detection = data.detections[0];

          // 🔹 Pause before sending anything
          const snap = takeSnapshot();
          if (snap) {
            setSnapshot(snap);
            setPaused(true);
            isPaused.current = true;

            // Tell backend to pause
            wsRef.current?.send("pause");

            // Resume after 5 seconds
            pauseTimer.current = setTimeout(() => {
              setPaused(false);
              setSnapshot(null);
              isPaused.current = false;

              wsRef.current?.send("resume");
            }, 3000);
          } else {
            // if snapshot failed, still set paused to prevent duplicates
            setPaused(true);
            isPaused.current = true;
          }

          // Only now send detection once
          const detectionPayload = {
            detected_class: detection.detected_class,
            category: detection.category,
          };

          onDetection && onDetection(detectionPayload);
          latestDetection.current = detectionPayload;
          await sendDetection(detectionPayload);
        }
      } catch (err) {
        console.error("❌ Failed to parse WebSocket message:", err);
      }
    };

    return () => {
      ws.close();
      if (pauseTimer.current) clearTimeout(pauseTimer.current);
    };
  }, [onDetection]);

  return (
    <div className="relative w-full flex items-center justify-center">
      {loading && !error && (
        <div className="absolute inset-0 flex items-center justify-center bg-white/60 rounded-lg z-20">
          <div className="w-10 h-10 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
        </div>
      )}

      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-white/60 rounded-lg z-1">
          <div className="text-red-500 font-medium text-center p-4">{error}</div>
        </div>
      )}

      <canvas ref={canvasRef} style={{ display: "none" }} />

      <div className="relative w-[640px] h-[480px] flex items-center justify-center">
        {/* Live feed always in background */}
        <img
          ref={imgRef}
          src="http://localhost:8000/camera/mjpeg"
          crossOrigin="anonymous"
          alt="Camera Feed"
          className="rounded-lg border w-full h-full object-cover"
          onLoad={() => setLoading(false)}
          onError={() => {
            setError("Unable to load camera feed");
            setLoading(false);
          }}
        />

        {/* Snapshot overlay centered */}
        {paused && snapshot && (
          <img
            src={snapshot}
            alt="Snapshot Overlay"
            className="absolute top-0 left-0 w-full h-full object-cover rounded-lg opacity-90 pointer-events-none z-1"
          />
        )}

        {/* Pause message centered */}
        {paused && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/40 text-white text-2xl font-bold rounded-lg z-1">
            Paused for 3s
          </div>
        )}
      </div>
    </div>
  );
};

export default CameraFrame;