import React from 'react'

const Sidebar = () => {
    return (
        <div className="drawer-side overflow-hidden">
            <label htmlFor="my-drawer" aria-label="close sidebar" className="drawer-overlay"></label>
            <ul className="menu bg-base-100 text-base-content min-h-full w-80 p-4">
                {/* Header Section */}
                <div className="flex flex-col items-center mb-4">
                    <img
                        src="/logo.png" // <-- replace with your logo path
                        alt="Logo"
                        className="w-16 h-16"
                    />
                    <h2 className="text-lg font-bold">SortAMatic Machine</h2>
                </div>
                <hr />
                <li><a href="/">Dashboard</a></li>
                <li><a href="/settings">Manual Control</a></li>
            </ul>
        </div>
    )
}

export default Sidebar