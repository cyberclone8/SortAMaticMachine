import React from 'react'
import CameraFrame from '../components/CameraFrame'
import { Camera, ClipboardClock } from 'lucide-react';
import SegreationLogs from '../components/SegreationLogs';
import BinStatus from '../components/BinStatus';

const MainPage = () => {
  return (
    <div className="grid grid-cols-3 gap-3 h-[900px] w-[1400px] p-6">
      {/* Camera Feed */}
      <div className="bg-white col-span-2 row-span-2 flex flex-col shadow-sm rounded-lg h-[580px]">
        <div className="flex gap-2 p-2 h-12 items-center">
          <Camera />
          <span>Camera Feed</span>
        </div>
        <div className="flex-1 flex items-center justify-center">
          <CameraFrame />
        </div>
      </div>

      {/* Segregation Logs */}
      <div className="bg-white row-span-2 flex flex-col shadow-sm rounded-lg h-[580px] ">
        {/* Header */}
        <div className="flex gap-2 p-2 h-12 items-center">
          <ClipboardClock />
          <span>Segregation Logs</span>
        </div>
        {/* Scrollable Logs */}
        <div className="flex-1 overflow-y-auto py-4">
          <SegreationLogs />
        </div>
      </div>

      {/* Bin Status */}
      <div className="bg-white col-span-2 flex flex-col shadow-sm rounded-lg h-[280px]">
        <div className="w-full h-full flex flex-col">
          {/* Header */}
          <div className="flex gap-2 p-2 h-12 items-center">
            <ClipboardClock />
            <span>Bin Status and Monitoring</span>
          </div>
          {/* Content */}
          <div className="flex-1 p-4 flex items-center justify-center">
            {/* Put your bin status content here */}
            <div className='w-full h-full rounded-sm'>
              <BinStatus />
            </div>
          </div>
        </div>
      </div>

      {/* Logo / Misc Card */}
      <div className="bg-white flex flex-col shadow-sm rounded-lg h-[280px]">
        <div className="w-full h-full flex flex-col">
          {/* Header */}
          <div className="flex gap-2 p-2 h-12 items-center">
            <ClipboardClock />
            <span>Logo / Info</span>
          </div>
          {/* Content */}
          <div className="flex-1 p-4 flex items-center justify-center">
            {/* Put logo or other info here */}
            <p>Logo goes here</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MainPage;
