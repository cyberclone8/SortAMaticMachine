import Navbar from "../components/Navbar";
import { Outlet } from "react-router-dom";

const MainLayout = () => {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Navbar */}
      <Navbar />

      {/* Main content */}
      <main className="flex-1 flex items-center justify-center bg-base-100 overflow-hidden">
        <Outlet /> {/* Pages will always be centered */}
      </main>
    </div>
  );
};

export default MainLayout;
