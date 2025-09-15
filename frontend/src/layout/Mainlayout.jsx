import Navbar from "../components/Navbar";
import { Outlet } from "react-router-dom";

const MainLayout = () => {
  return (
    <div className="flex flex-col h-screen">
      {/* Navbar fixed height */}
      <Navbar />

      {/* Main content scrollable */}
      <main className="flex-1 overflow-y-auto bg-base-100">
        <Outlet />
      </main>
    </div>
  );
};

export default MainLayout;