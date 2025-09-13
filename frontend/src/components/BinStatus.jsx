import React, { useState, useEffect } from "react";

const BinStatus = () => {
  // Each bin has its own percentage
  const [bin1, setBin1] = useState(20);
  const [bin2, setBin2] = useState(55);
  const [bin3, setBin3] = useState(75);
  const [bin4, setBin4] = useState(95);

  // Example: Simulate fetching API data every 5s
  useEffect(() => {
    const interval = setInterval(() => {
      // Replace this with your API fetch for each bin
      setBin1(Math.floor(Math.random() * 100));
      setBin2(Math.floor(Math.random() * 100));
      setBin3(Math.floor(Math.random() * 100));
      setBin4(Math.floor(Math.random() * 100));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getColor = (percent) => {
    if (percent < 50) return "bg-green-500";
    if (percent < 80) return "bg-yellow-500";
    return "bg-red-500"
  };

  return (
    <div className="grid grid-cols-4 gap-4 w-full h-full">
      {/* Bin 1 */}
      <div className="relative flex flex-col items-center justify-end shadow-sm rounded-lg overflow-hidden bg-gray-100">
        <div
          className={`absolute bottom-0 left-0 w-full transition-all duration-700 ease-in-out ${getColor(
            bin1
          )}`}
          style={{ height: `${bin1}%`, animation: "wave 2s infinite linear" }}
        ></div>
        <div className="relative z-10 text-center p-2 font-bold text-gray-700">
          {bin1}%
        </div>
      </div>

      {/* Bin 2 */}
      <div className="relative flex flex-col items-center justify-end shadow-sm rounded-lg overflow-hidden bg-gray-100">
        <div
          className={`absolute bottom-0 left-0 w-full transition-all duration-700 ease-in-out ${getColor(
            bin2
          )}`}
          style={{ height: `${bin2}%`, animation: "wave 2s infinite linear" }}
        ></div>
        <div className="relative z-10 text-center p-2 font-bold text-gray-700">
          {bin2}%
        </div>
      </div>

      {/* Bin 3 */}
      <div className="relative flex flex-col items-center justify-end shadow-sm rounded-lg overflow-hidden bg-gray-100">
        <div
          className={`absolute bottom-0 left-0 w-full transition-all duration-700 ease-in-out ${getColor(
            bin3
          )}`}
          style={{ height: `${bin3}%`, animation: "wave 2s infinite linear" }}
        ></div>
        <div className="relative z-10 text-center p-2 font-bold text-gray-700">
          {bin3}%
        </div>
      </div>

      {/* Bin 4 */}
      <div className="relative flex flex-col items-center justify-end  rounded-lg overflow-hidden bg-gray-100">
        <div
          className={`absolute bottom-0 left-0 w-full transition-all duration-700 ease-in-out ${getColor(
            bin4
          )}`}
          style={{ height: `${bin4}%`, animation: "wave 2s infinite linear" }}
        ></div>
        <div className="relative z-10 text-center p-2 font-bold text-gray-700">
          {bin4}%
        </div>
      </div>
    </div>
  );
};

export default BinStatus;
