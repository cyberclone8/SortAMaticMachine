import React, { useEffect, useState } from "react";

const SegregationLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  // Dummy actions to simulate
  const dummyActions = [
    { action: "Scanning Item...", category: null },
    { action: "Identified Item", category: "Metal - Can" },
    { action: "Segregating into Bin", category: "Metal Bin" },
    { action: "Success! Item Segregated", category: "Completed" },
  ];

  useEffect(() => {
    let step = 0;
    setLoading(true);

    const interval = setInterval(() => {
      if (step < dummyActions.length) {
        const newLog = {
          id: Date.now(),
          ...dummyActions[step],
          time: new Date().toISOString(),
        };

        setLogs((prev) => [...prev, newLog]); // prepend new log
        step++;

        // Stop loading after final success
        if (step === dummyActions.length) {
          setLoading(false);
        }
      } else {
        clearInterval(interval);
      }
    }, 5000); // every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      {/* Logs container */}
      <div className="flex-1 overflow-y-auto space-y-3">
        {logs.length > 0 ? (
          logs.map((log) => (
            <div
              key={log.id}
              className="p-3 rounded-lg border flex justify-between items-center bg-gray-50"
            >
              <div>
                <p className="font-medium">
                  {log.category ? log.category : "Processing..."}
                </p>
                <p className="text-sm text-gray-500">{log.action}</p>
              </div>
              <span className="text-xs text-gray-400">
                {new Date(log.time).toLocaleTimeString()}
              </span>
            </div>
          ))
        ) : (
          <p className="text-gray-500 text-center">No logs yet...</p>
        )}
      </div>

      {/* Loading indicator */}
      {loading && (
        <div className="mt-4 flex items-center justify-center">
          <div className="w-6 h-6 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
          <span className="ml-2 text-gray-500">Processing actions...</span>
        </div>
      )}
    </div>
  );
};

export default SegregationLogs;
