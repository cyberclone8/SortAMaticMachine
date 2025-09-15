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
    if (percent < 50) return "bg-green-300";
    if (percent < 80) return "bg-yellow-300";
    return "bg-red-300"
  };

  return (
    <div className="grid grid-cols-4 gap-4 w-full h-full">
      <div className="flex flex-col items-center">
        <div className="mb-2 font-semibold text-gray-800">Biodegradable</div>
        <div className="relative flex flex-col items-center justify-end w-full h-full bg-gray-200 rounded-b-xl overflow-hidden">
          {/* Bin Lid */}
          <div className="absolute -top-2 w-full h-4 bg-gray-400 rounded-t-lg shadow-sm"></div>
          <div
            className={`absolute bottom-0 left-0 w-full transition-all duration-700 ease-in-out ${getColor(
              bin1
            )}`}
            style={{
              height: `${bin1}%`,
              animation: "wave 2s infinite linear",
            }}
          ></div>
          <div className="relative z-10 text-center p-2 font-bold text-gray-700">
            {bin1}%
          </div>
        </div>
      </div>

      {/* Bin 2 */}
      <div className="flex flex-col items-center">
        <div className="mb-2 font-semibold text-gray-800">Non-biodegradable</div>
        <div className="relative flex flex-col items-center justify-end w-full h-full bg-gray-200 rounded-b-xl overflow-hidden">
          <div className="absolute -top-2 w-full h-4 bg-gray-400 rounded-t-lg shadow-sm"></div>
          <div
            className={`absolute bottom-0 left-0 w-full transition-all duration-700 ease-in-out ${getColor(
              bin2
            )}`}
            style={{
              height: `${bin2}%`,
              animation: "wave 2s infinite linear",
            }}
          ></div>
          <div className="relative z-10 text-center p-2 font-bold text-gray-700">
            {bin2}%
          </div>
        </div>
      </div>

      {/* Bin 3 */}
      <div className="flex flex-col items-center">
        <div className="mb-2 font-semibold text-gray-800">Recyclable</div>
        <div className="relative flex flex-col items-center justify-end w-full h-full bg-gray-200 rounded-b-xl overflow-hidden">
          <div className="absolute -top-2 w-full h-4 bg-gray-400 rounded-t-lg shadow-sm"></div>
          <div
            className={`absolute bottom-0 left-0 w-full transition-all duration-700 ease-in-out ${getColor(
              bin3
            )}`}
            style={{
              height: `${bin3}%`,
              animation: "wave 2s infinite linear",
            }}
          ></div>
          <div className="relative z-10 text-center p-2 font-bold text-gray-700">
            {bin3}%
          </div>
        </div>
      </div>

      {/* Bin 4 */}
      <div className="flex flex-col items-center">
        <div className="mb-2 font-semibold text-gray-800">Paper</div>
        <div className="relative flex flex-col items-center justify-end w-full h-full bg-gray-200 rounded-b-xl overflow-hidden">
          <div className="absolute -top-2 w-full h-4 bg-gray-400 rounded-t-lg shadow-sm"></div>
          <div
            className={`absolute bottom-0 left-0 w-full transition-all duration-700 ease-in-out ${getColor(
              bin4
            )}`}
            style={{
              height: `${bin4}%`,
              animation: "wave 2s infinite linear",
            }}
          ></div>
          <div className="relative z-10 text-center p-2 font-bold text-gray-700">
            {bin4}%
          </div>
        </div>
      </div>
    </div>
  );
};

export default BinStatus;
