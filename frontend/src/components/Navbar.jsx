import React from 'react'
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