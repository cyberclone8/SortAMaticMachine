import React, { useState } from "react";

const CameraFrame = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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
          <div className="text-red-500 font-medium text-center p-4">
            {error}
          </div>
        </div>
      )}

      {/* Camera stream */}
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
