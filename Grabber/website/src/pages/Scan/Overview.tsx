import { Row, Col, Card, Typography, Space, Skeleton } from "antd";
import { UserOutlined, BankOutlined, MailOutlined } from "@ant-design/icons";
import { FaComputer, FaTimeline } from "react-icons/fa6";

// Assuming user represents your user data
const user = {
  name: "John Doe",
  company: "Tech Solutions Inc.",
  email: "john.doe@example.com",
  bio: "Experienced software engineer with a strong background in web development.",

  os: "Windows 10",
  timestamp: new Date().toUTCString(),
  // Add more user data here
};

type OverviewProps = {
  client: ClientType;
  loading: boolean;
};
const Overview: React.FC<OverviewProps> = ({ client, loading }) => {
  return (
    <div>
      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card title="Basic Information" className="info-card">
            {loading && (
              <Skeleton active paragraph={{ rows: 4 }} className="mb-4" />
            )}
            {!loading && (
              <Space direction="vertical">
                <Typography.Title level={4}>
                  <UserOutlined /> {client.name}
                </Typography.Title>
                <Typography.Text type="secondary">{user.bio}</Typography.Text>
                <Typography.Text strong>
                  <BankOutlined /> Company:
                </Typography.Text>
                <Typography.Text>{client.company}</Typography.Text>
                <Typography.Text strong>
                  <MailOutlined /> Email:
                </Typography.Text>
                <Typography.Text>{client.email}</Typography.Text>
              </Space>
            )}
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Additional Information" className="info-card">
            {loading && (
              <Skeleton active paragraph={{ rows: 2 }} className="mb-4" />
            )}
            {!loading && (
              <Space direction="vertical">
                <Typography.Text className="flex items-center flex-row gap-2">
                  <FaComputer /> OS:
                </Typography.Text>
                <Typography.Text>{user.os}</Typography.Text>
                <Typography.Text className="flex items-center gap-2">
                  <FaTimeline /> Timestamp:
                </Typography.Text>
                <Typography.Text>{client.timestamp}</Typography.Text>
              </Space>
            )}
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Overview;
