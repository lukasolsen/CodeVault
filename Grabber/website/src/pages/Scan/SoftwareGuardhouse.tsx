import React, { useEffect, useState } from "react";
import {
  Tabs,
  Card,
  Typography,
  Space,
  Descriptions,
  Button,
  Input,
  message,
  Tooltip,
} from "antd";
import { CopyOutlined, QuestionCircleOutlined } from "@ant-design/icons";
import { getScanDiscord } from "../../service/api";
import { useLocation } from "react-router-dom";

const { TabPane } = Tabs;

const SoftwareGuardhouse = () => {
  const [activeTab, setActiveTab] = useState("discord");
  const [discordData, setDiscordData] = useState({} as any);

  const handleTabChange = (key) => {
    setActiveTab(key);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    message.success("Copied to clipboard!");
  };

  const pathname = useLocation();

  useEffect(() => {
    const getData = async () => {
      const name = new URLSearchParams(pathname.search).get("id");
      const res = await getScanDiscord(name || "");
      console.log("Token:", res.discord.token[0]);
      console.log(res);
      setDiscordData(res);
    };
    getData();
  }, []);

  const renderHelpButton = (property, helpText) => (
    <Tooltip title={helpText}>
      <Button icon={<QuestionCircleOutlined />} />
    </Tooltip>
  );

  const renderContent = () => {
    switch (activeTab) {
      case "discord":
        return (
          <Card title="Discord Information">
            <Descriptions column={2}>
              <Descriptions.Item label="Token">
                <Space>
                  <Input
                    defaultValue={discordData?.discord?.token[0] || ":("}
                    value={discordData?.discord?.token[0] || ":("}
                    disabled
                  />
                  <Button
                    icon={<CopyOutlined />}
                    onClick={() =>
                      copyToClipboard(discordData?.discord?.token[0])
                    }
                  />
                  {renderHelpButton(
                    "Token",
                    "Discord tokens are sensitive. Do not share them."
                  )}
                </Space>
              </Descriptions.Item>
              {/* Add more Discord-specific information here */}
            </Descriptions>
          </Card>
        );
      case "outlook":
        return (
          <Card title="Outlook Information">
            <Descriptions column={1}>
              <Descriptions.Item label="Example Property">
                Example Value
              </Descriptions.Item>
              <Descriptions.Item label="Help">
                <Button>
                  <QuestionCircleOutlined />
                  Learn more about Outlook properties
                </Button>
              </Descriptions.Item>
              {/* Add more Outlook-specific information here */}
            </Descriptions>
          </Card>
        );
      default:
        return null;
    }
  };

  return (
    <div style={{ padding: 24 }}>
      <Tabs activeKey={activeTab} onChange={handleTabChange}>
        <TabPane tab="Discord" key="discord">
          {renderContent()}
        </TabPane>
        <TabPane tab="Outlook" key="outlook">
          {renderContent()}
        </TabPane>
        {/* Add more tabs for other software as needed */}
      </Tabs>
    </div>
  );
};

export default SoftwareGuardhouse;
