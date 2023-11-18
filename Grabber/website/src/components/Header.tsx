import { Breadcrumb, Skeleton, Space, Flex, Typography } from "antd";
import { Header } from "antd/es/layout/layout";
import { Link } from "react-router-dom";

type HeaderProps = {
  loading: boolean;
  client: ClientType;
};

export const HeaderScan: React.FC<HeaderProps> = ({ client, loading }) => {
  return (
    <Header className="bg-gray-100 dark:bg-gray-800 h-full w-full p-1">
      {loading && <Skeleton title />}
      {!loading && (
        <>
          <Breadcrumb>
            <Breadcrumb.Item>
              <Link to="/">Home</Link>
            </Breadcrumb.Item>
            <Breadcrumb.Item>
              <Link to="/clients">Clients</Link>
            </Breadcrumb.Item>
            <Breadcrumb.Item>{client?.name}</Breadcrumb.Item>
          </Breadcrumb>

          <Space
            direction="horizontal"
            align="center"
            className="justify-between w-full"
            size="middle"
          >
            <Flex vertical>
              {"InCol" && (
                <Typography.Text type="secondary" className="text-gray-600">
                  Collection: <Link to="/collections">Malware</Link>
                </Typography.Text>
              )}
            </Flex>
            <Flex vertical>
              <Flex gap={2} align="center" justify="space-between">
                <Typography.Text strong>Analyzed:</Typography.Text>{" "}
                {new Date(client.timestamp).toUTCString()}
              </Flex>
            </Flex>
          </Space>
        </>
      )}
    </Header>
  );
};

export default HeaderScan;
