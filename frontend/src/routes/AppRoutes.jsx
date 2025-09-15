import { createBrowserRouter, RouterProvider } from "react-router-dom";
import MainLayout from "../layout/Mainlayout";
import MainPage from "../pages/MainPage";
import NotFound from "../components/404NotFound";
import ManualControl from "../components/ManualControl";

const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />, // Wraps all pages with navbar + drawer
    children: [
      {
      index: true,
      element: <MainPage />,
    },
    { 
      path: "manual-control", // "/manual-control"
      element: <ManualControl />,
    }
  ],
    errorElement: <NotFound />,
  },
]);

const AppRouter = () => <RouterProvider router={router} />;

export default AppRouter;