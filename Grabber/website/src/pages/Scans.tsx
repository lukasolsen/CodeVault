import {
  Layout,
  Typography,
  Row,
  Col,
  Card,
  List,
  Button,
  Divider,
  Flex,
} from "antd";
import { FileSearchOutlined, MailOutlined } from "@ant-design/icons";
import { useEffect, useState } from "react";
import { FaPlus } from "react-icons/fa";
import { getScans } from "../service/api";
import { Link } from "react-router-dom";

const { Content } = Layout;

type Scan = {
  _id: number;
  name: string;
  description: string;
  tags: string;
};

const Scans: React.FC = () => {
  const [scans, setScans] = useState<Scan[]>([]);

  useEffect(() => {
    const getData = async () => {
      const data = await getScans();
      setScans(data);
    };

    getData();
  }, []);

  return (
    <Content style={{ padding: "20px" }}>
      <Flex justify="space-between" align="center">
        <Typography.Title level={2}>Scans</Typography.Title>
        <Link to="/addclient">
          <Button type="text">
            <FaPlus />
          </Button>
        </Link>
      </Flex>
      <Divider />

      <Row gutter={[16, 16]}>
        {scans.length === 0 && (
          <Col span={24}>
            <Typography.Text type="secondary">No scans found</Typography.Text>
          </Col>
        )}
        {scans.length !== 0 &&
          scans.map((client) => (
            <Col span={8} key={client._id}>
              <Card
                title={client.name}
                actions={[
                  <Link to={"/scan?id=" + client._id}>
                    <Button icon={<FileSearchOutlined />} type="primary">
                      Details
                    </Button>
                  </Link>,
                ]}
              >
                <Typography.Text>{client.description}</Typography.Text>
              </Card>
            </Col>
          ))}
      </Row>

      <Divider />

      <Typography.Title level={3}>Scan List</Typography.Title>
      <List
        size="large"
        bordered
        dataSource={scans}
        renderItem={(client) => (
          <List.Item>
            <List.Item.Meta
              title={client.name}
              description={client.description}
            />
            {/* Add actions or details button here */}
          </List.Item>
        )}
      />
    </Content>
  );
};

export default Scans;
