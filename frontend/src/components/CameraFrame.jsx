import React, { useEffect, useRef, useState } from "react";

const CameraFrame = () => {
    const videoRef = useRef(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const startCamera = async () => {
            console.log("Requesting camera...");

            try {
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    setError("Your browser does not support camera access.");
                    setLoading(false);
                    return;
                }

                const stream = await navigator.mediaDevices.getUserMedia({ video: true });

                if (videoRef.current) {
                    videoRef.current.srcObject = stream;

                    videoRef.current.onloadeddata = () => {
                        console.log("Camera stream loaded ✅");
                        setLoading(false);
                    };

                }
            } catch (err) {
                console.error("Error accessing camera:", err);
                setError(`Unable to access camera: ${err.message}`);
                setLoading(false);
            }
        };

        startCamera();

        return () => {
            if (videoRef.current && videoRef.current.srcObject) {
                const tracks = videoRef.current.srcObject.getTracks();
                tracks.forEach((track) => track.stop());
            }
        };
    }, []);

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

            {/* Video centered */}
            <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="max-w-full max-h-[500px] object-contain rounded-lg"
            />
        </div>

    );

};

export default CameraFrame;
