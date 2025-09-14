import React from 'react'
import CameraFrame from '../components/CameraFrame'
import { Camera } from 'lucide-react';
import SegreationLogs from '../components/SegreationLogs';

const MainPage = () => {
  return (
    <div className="grid grid-cols-3 gap-3 h-[900px] w-[1400px] p-6">
      {/* Camera here */}
      <div className="bg-white col-span-2 row-span-2 flex flex-col shadow-sm rounded-lg">
        <div className="flex gap-2 p-2">
          <Camera />
          <span>Camera Feed</span>
        </div>

        <div className="flex-1 flex items-center justify-center ">
          <CameraFrame />
        </div>
      </div>

      {/* Logs here */}
      <div className="bg-white  row-span-2 flex flex-col shadow-sm rounded-lg">
        <div className="flex gap-2 p-2">
          <Camera />
          <span>Segregation Logs</span>
        </div>
        <div className="flex-1 bg-white p-4 shadow-sm rounded-lg h-full flex flex-col justify-center ">
          <SegreationLogs />
        </div>
      </div>

      {/* bin status here */}
      <div className="bg-white  col-span-2 p-6 shadow-sm rounded-lg">
        Card 3 - Bottom Wide
      </div>

      {/* logo here */}
      <div className="bg-white  p-6 shadow-sm rounded-lg">
        Card 4 - Bottom Wide

      </div>
    </div>
  )
}

export default MainPage