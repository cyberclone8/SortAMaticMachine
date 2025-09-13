import React, { useEffect, useState, useRef } from "react";

const SegregationLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  const dummyActions = [
    { action: "Scanning Item...", category: null },
    { action: "Identified Item", category: "Metal - Can" },
    { action: "Segregating into Bin", category: "Metal Bin" },
    { action: "Success! Item Segregated", category: "Completed" },
    { action: "Success! Item Segregated", category: "Completed" },
    { action: "Success! Item Segregated", category: "Completed" },
    { action: "Success! Item Segregated", category: "Completed" },
    { action: "Success! Item Segregated", category: "Completed" },
    { action: "Success! Item Segregated", category: "Completed" },
    { action: "Success! Item Segregated", category: "Completed" },
  ];

  useEffect(() => {
    let step = 0;
    setLoading(true);

    const interval = setInterval(() => {
      if (step < dummyActions.length) {
        const newLog = {
          id: Date.now() + step,
          ...dummyActions[step],
          time: new Date().toISOString(),
        };
        setLogs((prev) => [...prev, newLog]);
        step++;
        if (step === dummyActions.length) setLoading(false);
      } else {
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval);
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
