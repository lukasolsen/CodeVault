import { Avatar, Button, Divider, Dropdown, Flex, Typography } from "antd";
import { Header } from "antd/es/layout/layout";
import { useEffect, useState } from "react";
import { RiMoonClearLine, RiSunLine } from "react-icons/ri";
import { FaUser } from "react-icons/fa";
import { useAuth } from "../context/AuthContext";
import Link from "antd/es/typography/Link";
import { MenuFoldOutlined, MenuUnfoldOutlined } from "@ant-design/icons";
import { useClientNavbar } from "../context/ClientNavbarContext";

type NavbarProps = {
  isInClient: boolean;
};

const Navbar: React.FC<NavbarProps> = ({ isInClient }) => {
  const [darkMode, setDarkMode] = useState<boolean>(false);
  const { checkToken, isLoggedIn, userDetails } = useAuth();

  useEffect(() => {
    setDarkMode(document.documentElement.classList.contains("dark"));

    checkToken();
  }, []);

  const { collapsed, toggleCollapsed } = useClientNavbar();

  return (
    <Header style={{ backgroundColor: "transparent", alignItems: "center" }}>
      <Flex justify="space-between" align="center">
        <Flex justify="space-between" align="center" gap={10}>
          {isInClient === true && (
            <Button
              type="primary"
              onClick={toggleCollapsed}
              style={{ marginBottom: 16 }}
            >
              {collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            </Button>
          )}
          <Typography.Title level={2} style={{ lineHeight: 2 }}>
            Grabber
          </Typography.Title>
        </Flex>

        <Flex gap={10}>
          <Link href="/">
            <Button type="text">Home</Button>
          </Link>
          <Link href="/scans">
            <Button type="text">Scans</Button>
          </Link>
          <Button type="text">History</Button>
        </Flex>

        <Flex gap={10}>
          <Button
            type="text"
            onClick={() => {
              document.documentElement.classList.toggle("dark");
              setDarkMode(!darkMode);
            }}
          >
            {!darkMode ? <RiSunLine /> : <RiMoonClearLine />}
          </Button>
          {isLoggedIn ? (
            <Dropdown
              align={{ offset: [0, 10] }}
              overlay={
                <Flex vertical>
                  <Flex vertical>
                    <Typography.Text>{userDetails?.name}</Typography.Text>
                    <Typography.Text type="secondary">
                      {userDetails?.email}
                    </Typography.Text>
                  </Flex>
                  <Divider />
                  <Button
                    type="primary"
                    onClick={() => {
                      location.href = "/logout";
                    }}
                  >
                    Logout
                  </Button>
                </Flex>
              }
            >
              <a onClick={(e) => e.preventDefault()}>
                <Avatar
                  className="flex justify-center items-center"
                  children={<FaUser />}
                />
              </a>
            </Dropdown>
          ) : (
            <Button
              type="default"
              onClick={() => {
                location.href = "/login";
              }}
            >
              Sign in
            </Button>
          )}
        </Flex>
      </Flex>
    </Header>
  );
};

export default Navbar;
