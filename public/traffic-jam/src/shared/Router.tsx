import { createBrowserRouter } from "react-router-dom";
import ErrorPage from "./pages/error/error";
import Register from "./pages/registration/registration";
import Home from "./pages/home/home";
import App from "../App"
import Login from "./pages/login/login";
import Map from "./pages/map/map";
import Users from "./pages/users/users";

const Router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "home",
        element: <Home />
      },
      {
        path: "register",
        element: <Register />
      },
      {
        path: "login",
        element: <Login />
      },
      {
        path: "map",
        element: <Map />
      },
      {
        path: "users",
        element: <Users />
      }
    ]
  }
]);

export default Router;