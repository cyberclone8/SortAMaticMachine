import React, { useEffect, useState, useRef } from "react";
import { sendDetection } from "../utils/sendDetection";

const SegregationLogs = ({ detection }) => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (!detection) return;

    const processDetection = async () => {
      setLoading(true);

      const scanningLog = {
        id: Date.now(),
        action: "Scanning Item...",
        category: null,
        time: new Date().toISOString(),
        type: "info", // use type to control color
      };

      setLogs((prev) => [...prev, scanningLog].slice(-15));

      try {
        const result = await sendDetection(detection); // { status, classification, object }

        const newLogs = [
          {
            id: Date.now() + 1,
            action: "Identified Item",
            category: result.object,
            time: new Date().toISOString(),
            type: "info",
          },
          {
            id: Date.now() + 2,
            action: "Segregating into Bin",
            category: `${result.classification} Bin`,
            time: new Date().toISOString(),
            type: "info",
          },
          {
            id: Date.now() + 3,
            action: "Success! Item Segregated",
            category: "Completed",
            time: new Date().toISOString(),
            type: "success", // completed log
          },
        ];

        setLogs((prev) => [...prev, ...newLogs].slice(-15));
      } catch (err) {
        console.error("Error sending detection:", err);
        const errorLog = {
          id: Date.now(),
          action: "Error processing detection",
          category: "Failed",
          time: new Date().toISOString(),
          type: "error",
        };
        setLogs((prev) => [...prev, errorLog].slice(-15));
      } finally {
        setLoading(false);
      }
    };

    processDetection();
  }, [detection]);

  // Auto scroll to bottom
  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [logs]);

  const getCategoryColor = (type) => {
    switch (type) {
      case "success":
        return "text-green-600";
      case "error":
        return "text-red-600";
      default:
        return "text-gray-800";
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div ref={scrollRef} className="flex-1 p-4 space-y-3 overflow-y-auto">
        {logs.length === 0 && (
          <p className="text-gray-500 text-center">No logs yet...</p>
        )}

        {logs.map((log) => (
          <div
            key={log.id}
            className="p-3 rounded-lg border flex justify-between items-center bg-gray-50"
          >
            <div>
              <p className={`font-medium ${getCategoryColor(log.type)}`}>
                {log.category || "Processing..."}
              </p>
              <p className="text-sm text-gray-500">{log.action}</p>
            </div>
            <span className="text-xs text-gray-400">
              {new Date(log.time).toLocaleTimeString()}
            </span>
          </div>
        ))}

        {loading && (
          <div className="flex items-center justify-center mt-2">
            <div className="w-6 h-6 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
            <span className="ml-2 text-gray-500">Processing actions...</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default SegregationLogs;