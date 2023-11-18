import React from "react";
import { AppstoreOutlined } from "@ant-design/icons";
import type { MenuProps } from "antd";
import { Menu } from "antd";
import {
  FaShieldVirus,
  FaNetworkWired,
  FaBinoculars,
  FaLock,
  FaCode,
} from "react-icons/fa6";
import { useClientNavbar } from "../context/ClientNavbarContext";

type MenuItem = Required<MenuProps>["items"][number];

function getItem(
  label: React.ReactNode,
  key: React.Key,
  icon?: React.ReactNode,
  children?: MenuItem[],
  type?: "group"
): MenuItem {
  return {
    key,
    icon,
    children,
    label,
    type,
  } as MenuItem;
}

const items: MenuItem[] = [
  getItem("Overview", "overview", <AppstoreOutlined />), // Overview
  getItem("Cyber Sentinel", "cyber-sentinel", <FaBinoculars />), // Browser Insights
  getItem("Vulnerability Reader", "vulnerability-reader", <FaShieldVirus />), // Threat Intelligence
  getItem("Network Activity", "network-activity", <FaNetworkWired />, [
    getItem("Overview", "network-activity-overview"),
    getItem("DNS Resolutions", "network-activity-dns"),
    getItem("TCP Requests", "network-activity-tcp"),
    getItem("UDP Requests", "network-activity-udp"),
    getItem("HTTP Requests", "network-activity-http"),
  ]), // Network Analysis
  getItem("Software Guardhouse", "software-guardhouse", <FaCode />), // Software Protection
  getItem("Data Guardian", "data-guardian", <FaLock />), // Data Protection
];

const ClientNavbar: React.FC = () => {
  const { setSelectedKey, collapsed, selectedKey } = useClientNavbar();

  const handleMenuItemSelect = ({ key }: { key: React.Key }) => {
    setSelectedKey(key.toString());
  };

  return (
    <div
      style={{
        width: collapsed ? 80 : 256,
        height: "100vh",
        overflowY: "auto",
      }}
    >
      <Menu
        selectedKeys={[selectedKey]}
        defaultOpenKeys={["sub1"]}
        mode="inline"
        theme="dark"
        inlineCollapsed={collapsed}
        items={items}
        onSelect={handleMenuItemSelect}
        style={{ height: "100%" }}
      />
    </div>
  );
};

export default ClientNavbar;
