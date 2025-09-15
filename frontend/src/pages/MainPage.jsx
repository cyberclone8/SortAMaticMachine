import React, {useState} from "react";
import CameraFrame from "../components/CameraFrame";
import { Camera, ClipboardClock } from "lucide-react";
import SegreationLogs from "../components/SegreationLogs";
import BinStatus from "../components/BinStatus";
import Logo from "../assets/Logo.jpg";

const MainPage = () => {
  const [latestDetection, setLatestDetection] = useState(null);
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="grid grid-cols-3 gap-3 h-[900px] w-[1400px] p-6">
        {/* Camera Feed */}
        <div className="bg-white col-span-2 row-span-2 flex flex-col shadow-sm rounded-lg h-[580px]">
          <div className="flex gap-2 p-2 h-12 items-center">
            <Camera />
            <span>Camera Feed</span>
          </div>
          <div className="flex-1 flex items-center justify-center">
            <CameraFrame onDetection={setLatestDetection} />
          </div>
        </div>

        {/* Segregation Logs */}
        <div className="bg-white row-span-2 flex flex-col shadow-sm rounded-lg h-[580px]">
          <div className="flex gap-2 p-2 h-12 items-center">
            <ClipboardClock />
            <span>Segregation Logs</span>
          </div>
          <div className="flex-1 overflow-y-auto py-4">
            <SegreationLogs detection={latestDetection} />
          </div>
        </div>

        {/* Bin Status */}
        <div className="bg-white col-span-2 flex flex-col shadow-sm rounded-lg h-[280px]">
          <div className="w-full h-full flex flex-col">
            <div className="flex gap-2 p-2 h-12 items-center">
              <ClipboardClock />
              <span>Bin Status and Monitoring</span>
            </div>
            <div className="flex-1 p-4 flex items-center justify-center">
              <div className="w-full h-full rounded-sm">
                <BinStatus />
              </div>
            </div>
          </div>
        </div>

        {/* Logo / Misc Card */}
        <div className="bg-white flex flex-col shadow-sm rounded-lg h-[280px]">
          <div className="w-full h-full flex flex-col">
            <div className="flex gap-2 p-2 h-12 items-center">
              <ClipboardClock />
              <span>Logo / Info</span>
            </div>
            <div className="flex-1 flex items-center justify-center flex-col text-center px-4">
              <img
                src={Logo}
                alt="Logo"
                className="w-20 h-20 md:w-32 md:h-32 rounded-full shadow-sm animate-spin-slow logo-flip"
              />
              <h1 className="text-lg font-bold text-gray-800">
                Sort-A-Matic Machine
              </h1>
              <p className="text-gray-600 text-sm max-w-full">
                An intelligent segregation system powered by real-time object
                detection and automation. Built for efficiency, accuracy, and
                innovation.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;