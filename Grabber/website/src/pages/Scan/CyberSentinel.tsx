import {
  Card,
  Col,
  Row,
  Typography,
  Empty,
  Menu,
  Flex,
  Switch,
  MenuProps,
} from "antd";
import {
  FileTextOutlined,
  FormOutlined,
  LockOutlined,
  DownloadOutlined,
  CreditCardOutlined,
} from "@ant-design/icons";
import { useEffect, useState } from "react";
import "react-data-grid/lib/styles.css";
import { getScanWebsiteType, getScanWebsitesPre } from "../../service/api";
import { useLocation } from "react-router-dom";
import BrowserTable from "../../components/BrowserTable";
type MenuItem = Required<MenuProps>["items"][number];

export const CyberSentinel: React.FC = () => {
  const [hideAll, setHideAll] = useState<boolean>(true);
  const [clientExists, setClientExists] = useState<boolean>(false);
  const [browserData, setBrowserData] = useState<[]>([]);
  const [selectedBrowserIndex, setSelectedBrowserIndex] = useState<number>(0);
  const [secondaryBrowserTab, setSecondaryBrowserTab] =
    useState<string>("autofill");

  const [displayData, setDisplayData] = useState<{
    data: {
      columns: string[];
      results: any;
    };
  }>({ data: { columns: [], results: [] } });

  const pathname = useLocation();
  const name = new URLSearchParams(pathname.search).get("id");

  useEffect(() => {
    const getData = async () => {
      getScanWebsitesPre(name || "").then((res) => {
        if (res.client == "Not found") {
          setClientExists(false);
          return;
        }
        setClientExists(true);
        console.log(res);
        setBrowserData(res);
      });
    };
    getData();
  }, []);

  useEffect(() => {
    getScanWebsiteType(
      name || "",
      browserData[selectedBrowserIndex]?.name || "chrome",
      secondaryBrowserTab.charAt(0).toUpperCase() + secondaryBrowserTab.slice(1)
    ).then((res) => {
      const { columns, results } = res;
      setDisplayData({ data: { columns, results } });
    });
  }, [name, browserData, selectedBrowserIndex, secondaryBrowserTab]);

  const getIconForValue = (value: string) => {
    switch (value) {
      case "Autofill":
        return <FileTextOutlined />;
      case "LoginData":
        return <FormOutlined />;
      case "Cookies":
        return <LockOutlined />;
      case "History":
        return <FileTextOutlined />;
      case "Downloads":
        return <DownloadOutlined />;
      case "Credit_Cards":
        return <CreditCardOutlined />;
      default:
        return null;
    }
  };

  // For the sub-menu
  const visibleBrowsers = hideAll
    ? browserData.filter((browser) =>
        Object.values(browser.data).some((value) => value > 0)
      )
    : browserData;

  const getVisibleBrowserChilds = (index: number) => {
    const browser = browserData[index];
    return hideAll
      ? Object.entries(browser.data || {}).filter(([_, value]) => value > 0)
      : Object.entries(browser.data || {});
  };

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

  const items: MenuProps["items"] = visibleBrowsers.map((browser, index) =>
    getItem(
      browser.name.charAt(0).toUpperCase() + browser.name.slice(1),
      browser.name,
      getIconForValue(browser.name),
      getVisibleBrowserChilds(index).map(([val, value]) => {
        return getItem(
          `${val} (${value})`,
          val + "-" + index,
          getIconForValue(val)
        );
      })
    )
  );

  return (
    <>
      {clientExists ? (
        <Row gutter={16}>
          <Col span={4}>
            <Flex justify="space-between" align="center">
              <Typography.Title level={4}>Browser</Typography.Title>
              <Switch
                checkedChildren="Hide All"
                unCheckedChildren="Show All"
                checked={hideAll}
                onChange={(value) => setHideAll(value)}
              />
            </Flex>
            <Menu
              mode="inline"
              defaultSelectedKeys={[
                browserData ? getVisibleBrowserChilds(0)[0] : "Autofill",
              ]}
              onSelect={({ key }) => {
                const [secondaryBrowserTab, index] = key.split("-");
                setSelectedBrowserIndex(Number(index));
                setSecondaryBrowserTab(secondaryBrowserTab);
              }}
              defaultOpenKeys={[visibleBrowsers[0]?.name]}
              style={{ borderRight: 0 }}
              onClick={({ key }) => setSecondaryBrowserTab(key.split("-")[0])}
              items={items}
            ></Menu>
          </Col>
          <Col span={18}>
            <Card
              title={
                <Flex justify="space-between">
                  <Typography.Text>
                    {browserData[selectedBrowserIndex]?.name
                      ?.charAt(0)
                      .toUpperCase() +
                      browserData[selectedBrowserIndex]?.name
                        .toString()
                        .slice(1) || "Chrome"}
                  </Typography.Text>
                </Flex>
              }
            >
              {displayData?.data?.columns?.length === 0 ? (
                <Typography.Text strong>No data found.</Typography.Text>
              ) : (
                <BrowserTable displayData={displayData} />
              )}
            </Card>
          </Col>
        </Row>
      ) : (
        <Empty />
      )}
    </>
  );
};
