import React, { useEffect, useState } from "react";
import { Card, List, Divider, Tooltip, Flex, Empty } from "antd";
import {
  EnvironmentOutlined,
  LockOutlined,
  GlobalOutlined,
  WifiOutlined,
  LaptopOutlined,
} from "@ant-design/icons";
import { FaInfoCircle } from "react-icons/fa";
import { getScanNetworkOverview } from "../../service/api";
import { useLocation } from "react-router-dom";

type NetworkData = {
  interfaces: {
    [interfaceName: string]: {
      inet: string | null;
      inet4: string[];
      ether: string | null;
      inet6: string[];
      netmask: string | null;
      netmasks: string[];
      broadcast: string | null;
      broadcasts: string[];
      prefixlens: string[];
      device: string;
      default_gateway: string | null;
      hostname: string | null;
    };
  };
  profiles: {
    name: string;
    password: string;
  }[];
};

const NetworkActivity: React.FC = () => {
  const [networkData, setNetworkData] = useState<NetworkData>(
    {} as NetworkData
  );

  const pathname = useLocation();

  useEffect(() => {
    const getData = async () => {
      const name = new URLSearchParams(pathname.search).get("id");
      const data = await getScanNetworkOverview(name || "");
      setNetworkData(data);
    };

    getData();
  }, []);

  return (
    <div className="container mx-auto my-8">
      {/* Title */}
      <h1 className="text-3xl font-semibold mb-4">Network Activity Overview</h1>

      {/* profiles Section */}
      <Card bordered={false}>
        <Divider orientation="left">
          <Flex gap={4} align="center">
            Profiles
            <Tooltip
              title={"All the networks that user has been connected to."}
            >
              <FaInfoCircle className="text-blue-500" />
            </Tooltip>
          </Flex>
        </Divider>
        {!networkData.profiles && <Empty description="No profiles found" />}
        {networkData.profiles && (
          <List
            dataSource={networkData.profiles}
            renderItem={(profile) => (
              <List.Item>
                <List.Item.Meta
                  title={profile.name}
                  description={
                    <p>
                      <LockOutlined /> Password: {profile.password}
                    </p>
                  }
                />
              </List.Item>
            )}
          />
        )}
      </Card>

      {/* Network interfaces Section */}
      <Card bordered={false} className="my-2">
        <Divider orientation="left">
          <Flex gap={4} align="center">
            Network interfaces
            <Tooltip title={"All the network interfaces on the device."}>
              <FaInfoCircle className="text-blue-500" />
            </Tooltip>
          </Flex>
        </Divider>

        {!networkData.interfaces && (
          <Empty description="No network interfaces found" />
        )}

        {networkData.interfaces && (
          <List
            itemLayout="horizontal"
            dataSource={Object.entries(networkData.interfaces)}
            renderItem={([interfaceName, data]) => (
              <List.Item>
                <List.Item.Meta
                  title={interfaceName}
                  description={
                    <div>
                      {data.inet && (
                        <p>
                          <GlobalOutlined /> IP: {data.inet || "N/A"}
                        </p>
                      )}
                      <p>
                        <WifiOutlined /> MAC Address: {data.ether || "N/A"}
                      </p>
                      <p>
                        <LaptopOutlined /> Device: {data.device || "N/A"}
                      </p>
                      {data.netmask && (
                        <p>
                          <GlobalOutlined /> Netmask: {data.netmask || "N/A"}
                        </p>
                      )}
                      {data.default_gateway && (
                        <p>
                          <GlobalOutlined /> Default Gateway:{" "}
                          {data.default_gateway || "N/A"}
                        </p>
                      )}
                      {data.hostname && (
                        <p>
                          <EnvironmentOutlined /> Hostname:{" "}
                          {data.hostname || "N/A"}
                        </p>
                      )}
                    </div>
                  }
                />
              </List.Item>
            )}
          />
        )}
      </Card>
    </div>
  );
};

export default NetworkActivity;
