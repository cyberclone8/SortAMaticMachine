import React from "react";
import { NavLink } from "react-router-dom";
import Logo from "../assets/Logo.jpg"; 

const Sidebar = () => {
  const closeDrawer = () => {
    const drawerCheckbox = document.getElementById("my-drawer");
    if (drawerCheckbox) drawerCheckbox.checked = false;
  };

  return (
    <div className="drawer-side overflow-hidden">
      <label
        htmlFor="my-drawer"
        aria-label="close sidebar"
        className="drawer-overlay"
      ></label>
      <ul className="menu bg-base-100 text-base-content min-h-full w-80 p-4">
        {/* Header Section */}
        <div className="flex flex-col items-center mb-4">
          <img
            src={Logo}
            alt="Logo"
            className="w-16 h-16 rounded-full"
          />
          <h2 className="text-lg font-bold">SortAMatic Machine</h2>
        </div>
        <hr />

        {/* Nav Items with NavLink */}
        <li>
          <NavLink
            to="/"
            onClick={closeDrawer} // 👈 close on click
            className={({ isActive }) =>
              isActive
                ? "bg-primary text-white rounded-lg px-3 py-2"
                : "px-3 py-2 rounded-lg"
            }
          >
            Dashboard
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/manual-control"
            onClick={closeDrawer} // 👈 close on click
            className={({ isActive }) =>
              isActive
                ? "bg-primary text-white rounded-lg px-3 py-2"
                : "px-3 py-2 rounded-lg"
            }
          >
            Manual Control
          </NavLink>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;