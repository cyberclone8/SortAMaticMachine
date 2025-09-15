import React, { useState, useEffect, useRef } from "react";
import { createSocket } from "../utils/createSocket";
import { sendDetection } from "../utils/sendDetection";

const CameraFrame = ({onDetection}) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const latestDetection = useRef(null); // store latest detection

  useEffect(() => {
    const ws = createSocket("ws://localhost:8000/ws/inference");

    ws.onopen = () => {
      console.log("WebSocket connected to /ws/inference");
      setLoading(false);
    };

    ws.onmessage = async (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.error) {
          setError(data.error);
          latestDetection.current = null;
        } else if (data.detected_class) {
          // Only keep the relevant fields
          const detectionPayload = {
            detected_class: data.detected_class,
            category: data.category
          };

          onDetection && onDetection(detectionPayload);

          latestDetection.current = detectionPayload;
          console.log("Latest detection:", latestDetection.current);

          // Send only the necessary fields to your API
          const result = await sendDetection(detectionPayload);
          console.log("API result:", result);
        }
      } catch (err) {
        console.error("Failed to parse WebSocket message:", err);
      }
    };

    return () => ws.close();
  }, [onDetection]);

  return (
    <div className="relative w-full flex items-center justify-center">
      {/* Loading overlay */}
      {loading && !error && (
        <div className="absolute inset-0 flex items-center justify-center bg-white/60 rounded-lg">
          <div className="w-10 h-10 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
        </div>
      )}

      {/* Error overlay */}
      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-white/60 rounded-lg">
          <div className="text-red-500 font-medium text-center p-4">{error}</div>
        </div>
      )}

      {/* Camera feed */}
      <img
        src="http://localhost:8000/camera/mjpeg"
        alt="Camera Feed"
        className="rounded-lg border w-[640px] h-[480px] object-cover"
        onLoad={() => setLoading(false)}
        onError={() => {
          setError("Unable to load camera feed");
          setLoading(false);
        }}
      />
    </div>
  );
};

export default CameraFrame;