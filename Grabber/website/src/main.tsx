import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LayoutApp from "./Layout/index.tsx";
import Client from "./pages/Scan.tsx";
import { AuthProvider } from "./context/AuthContext.tsx";
import { Register } from "./pages/Register.tsx";
import { Login } from "./pages/Login.tsx";
import { UserHome } from "./pages/UserHome.tsx";
import { ConfigProvider, theme } from "antd";
import AddClient from "./pages/AddClient.tsx";
import { ClientNavbarProvider } from "./context/ClientNavbarContext.tsx";
import Scans from "./pages/Scans.tsx";
import Scan from "./pages/Scan.tsx";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <BrowserRouter>
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,
        token: {
          colorBgContainer: "#0f1823",
          colorBgLayout: "#0f1823",
        },
        components: {
          Layout: {
            headerBg: "rgba(0,0,0,.2)",
          },
          Menu: {
            darkItemBg: "rgba(0,0,0,.2)",
            subMenuItemBg: "rgba(0,0,0,.3)",
            darkSubMenuItemBg: "rgba(0,0,0,.3)",
          },
          TreeSelect: {
            colorBgElevated: "#0f1823",
            colorBgContainer: "#0f1823",
          },
        },
      }}
    >
      <AuthProvider>
        <ClientNavbarProvider>
          <Routes>
            <Route element={<LayoutApp />}>
              <Route path="/" element={<App />} />
              <Route path="/scan" element={<Scan />} />
              <Route path="/register" element={<Register />} />
              <Route path="/login" element={<Login />} />
              <Route path="/user" element={<UserHome />} />
              <Route path="/scans" element={<Scans />} />
              <Route path="/addclient" element={<AddClient />} />
              <Route path="*" element={<h1>404</h1>} />
            </Route>
          </Routes>
        </ClientNavbarProvider>
      </AuthProvider>
    </ConfigProvider>
  </BrowserRouter>
);
