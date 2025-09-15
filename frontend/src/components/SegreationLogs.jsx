import React, { useEffect, useState, useRef } from "react";
import  {createSocket } from "../utils/createSocket";

const SegregationLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  const dummyActions = [
    { action: "Scanning Item...", category: null },
    { action: "Identified Item", category: "Metal - Can" },
    { action: "Segregating into Bin", category: "Metal Bin" },
    { action: "Success! Item Segregated", category: "Completed" },
  ];

  const socket = new WebSocket("ws://localhost:8080");

  useEffect(() => {
    let step = 0;
    socket.onopen = () => {
      setLoading(true);
    }

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        /**
         * Example messages from server:
         * { action: "Scanning Item...", category: null }
         * { action: "Identified Item", category: "Metal - Can" }
         * { action: "Segregating into Bin", category: "Metal Bin" }
         * { action: "Success! Item Segregated", category: "Completed" }
         */

        const newLog = {
          id: Date.now(),
          ...data,
          time: new Date().toISOString(),
        };

        // If new scanning starts → reset logs
        if (data.action === "Scanning Item...") {
          setLogs([newLog]);
        } else {
          setLogs((prev) => [...prev, newLog]);
        }

        // If completed → stop loader
        if (data.category === "Completed") {
          setLoading(false);
        } else {
          setLoading(true);
        }
      } catch (error) {
        console.error("Error parsing WebSocket message:", err);
      }

      socket.onclose = () => {
        setLoading(false);
      }
    }

    return () => socket.close();
  }, []);

  // Auto scroll to bottom
  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [logs]);

  return (
    <div className="flex flex-col h-full">
      {/* Scrollable logs */}
      <div
        ref={scrollRef}
        className="flex-1 p-4 space-y-3 overflow-y-auto"
      >
        {logs.length === 0 && <p className="text-gray-500 text-center">No logs yet...</p>}

        {logs.map((log) => (
          <div
            key={log.id}
            className="p-3 rounded-lg border flex justify-between items-center bg-gray-50"
          >
            <div>
              <p className="font-medium">{log.category || "Processing..."}</p>
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
