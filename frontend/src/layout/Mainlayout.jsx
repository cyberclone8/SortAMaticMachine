import React from 'react'
import Navbar from '../components/Navbar'
import MenuItems from '../components/MenuItems'

const Mainlayout = ({children}) => {
  return (
    <div>
      <div className="drawer lg:drawer-open min-h-screen">
      {/* Drawer toggle */}
      <input id="my-drawer" type="checkbox" className="drawer-toggle" />

      {/* Page content */}
      <div className="drawer-content flex flex-col">
        {/* Navbar always on top */}
        <Navbar />

        {/* Dashboard content below */}
        <main className="p-6 flex-1 bg-base-100">{children}</main>
      </div>

      {/* Sidebar */}
      <div className="drawer-side">
        <label htmlFor="my-drawer" className="drawer-overlay"></label>
        <ul className="menu p-4 w-64 min-h-full bg-base-200 text-base-content">
          <MenuItems />
        </ul>
      </div>
    </div>
    </div>
  )
}

export default Mainlayout
