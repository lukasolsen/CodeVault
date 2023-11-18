import React, { useEffect, useState } from "react";
import { getScan } from "../service/api";
import "react-data-grid/lib/styles.css";
import { Layout } from "antd";
import { useClientNavbar } from "../context/ClientNavbarContext";
import Overview from "./Scan/Overview";
import { CyberSentinel } from "./Scan/CyberSentinel";
import HeaderScan from "../components/Header";
import SoftwareGuardhouse from "./Scan/SoftwareGuardhouse";
import NetworkActivity from "./Scan/NetworkActivity";
import NetworkActivityType from "./Scan/NetworkActivityType";

const Scan: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const urlParams = new URLSearchParams(window.location.search);

  const [client, setClient] = useState<ClientType>({} as ClientType);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      // Example url: http://localhost:5173/user?name=1
      const id = urlParams.get("id");

      if (id) {
        const user = await getScan(id);
        console.log(user);
        setClient(user);
      }
      setLoading(false);
    };

    fetchData();
  }, []);

  const { selectedKey } = useClientNavbar();

  return (
    <Layout>
      <HeaderScan loading={loading} client={client} />

      <div className="container mx-auto mt-8">
        {selectedKey === "overview" && (
          <Overview client={client} loading={loading} />
        )}
        {selectedKey === "cyber-sentinel" && <CyberSentinel />}
        {selectedKey === "network-activity-overview" && <NetworkActivity />}
        {selectedKey === "network-activity-tcp" && (
          <NetworkActivityType type="tcp" />
        )}
        {selectedKey === "network-activity-udp" && (
          <NetworkActivityType type="udp" />
        )}
        {selectedKey === "network-activity-icmp" && (
          <NetworkActivityType type="icmp" />
        )}
        {selectedKey === "network-activity-arp" && (
          <NetworkActivityType type="arp" />
        )}
        {selectedKey === "network-activity-dns" && (
          <NetworkActivityType type="dns" />
        )}
        {selectedKey === "network-activity-http" && (
          <NetworkActivityType type="http" />
        )}
        {selectedKey === "software-guardhouse" && <SoftwareGuardhouse />}
      </div>
    </Layout>
  );
};

export default Scan;
