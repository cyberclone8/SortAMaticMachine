import { createBrowserRouter, RouterProvider } from "react-router-dom";
import MainLayout from "../layout/Mainlayout";
import MainPage from "../pages/MainPage";
import NotFound from "../components/404NotFound";

const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />, // Wraps all pages with navbar + drawer
    children: [{
      index: true,
      element: <MainPage />,
    }],
    errorElement: <NotFound />,
  },
]);

const AppRouter = () => <RouterProvider router={router} />;

export default AppRouter;