import React from 'react'
<<<<<<< HEAD
import { Menu } from "lucide-react"

export default function Navbar() {
  return (
    <div>
      <div className="navbar bg-base-100 shadow-sm">
        <div className="navbar-start">
           <Menu /> 
        </div>
        <div className="navbar-center">
            <a className="btn btn-ghost text-2xl">TITLE HERE</a>
        </div>
        <div className="navbar-end">
            <button className="btn btn-ghost btn-circle">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"> <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /> </svg>
            </button>
        </div>
        </div>
    </div>
  )
}
=======
import { Menu } from 'lucide-react'
import Sidebar from './Sidebar'

const Navbar = () => {
    return (
        <div>
            <div className="drawer">
                {/* Drawer Toggle */}
                <input id="my-drawer" type="checkbox" className="drawer-toggle" />

                <div className="drawer-content">
                    {/* Navbar */}
                    <div className="navbar bg-base-200 shadow">
                        {/* Left side (Hamburger Icon) */}
                        <div className="navbar-start">
                            <label htmlFor="my-drawer" className="btn btn-ghost">
                                <Menu size={26} />
                            </label>
                        </div>

                        {/* Center (Title) */}
                        <div className="navbar-center">
                            <a className="text-xl md:text-3xl font-bold">Sort-A-Matic Machine</a>
                        </div>
                        {/* Right side (Logo) */}
                        <div className="navbar-end">
                            <img
                                src="/logo.png"
                                alt="Logo"
                                className="w-8 h-8 md:w-10 md:h-10  rounded-full"
                            />
                        </div>
                    </div>
                </div>

                {/* Drawer Sidebar */}
                <Sidebar />
            </div>
        </div>
    )
}

export default Navbar
>>>>>>> 07056660920abd5b1e05ab10c2d225697d0307bb
