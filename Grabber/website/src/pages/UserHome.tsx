import { Button, Flex, Layout, TimePicker, Typography } from "antd";
import { Header } from "antd/es/layout/layout";

export const UserHome: React.FC = () => {
  return (
    <Layout>
      <Header style={{ alignItems: "center" }}>
        <Flex justify="space-between" align="center">
          <Typography.Title level={2} style={{ lineHeight: 2 }}>
            Detection & Response
          </Typography.Title>
          <TimePicker.RangePicker
            disabled
            style={{
              backgroundColor: "transparent",
              border: "none",
              borderBottom: "2px solid rgba(81,89,187,.35)",
              borderRadius: 0,
            }}
          />
        </Flex>
      </Header>
      <Layout>
        <Flex vertical>
          <Flex>
            <div className="bg-[rgba(33,43,73,.35)]">
              <h2 className="text-2xl font-bold text-white">0 Collections</h2>
            </div>
            <Flex vertical>
              <Typography.Title level={4}>Collections</Typography.Title>

              <Button type="primary">New Collection</Button>
            </Flex>
          </Flex>
        </Flex>
      </Layout>
    </Layout>
  );
};
