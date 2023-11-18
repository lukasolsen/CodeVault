import { Outlet, useLocation } from "react-router-dom";
import Navbar from "./Navbar";
import ClientNavbar from "./ClientNavbar";
import { Col, Layout, Row } from "antd";

const LayoutApp: React.FC = () => {
  const pathname = useLocation().pathname;

  return (
    <>
      <div className="dark:bg-dark-bg dark:text-white text-black bg-slate-100 dark:bg-[#0f1823] h-full min-h-screen break-all">
        <Navbar isInClient={pathname === "/scan"} />
        {pathname === "/scan" && (
          <Layout>
            <Row>
              <Col>
                <ClientNavbar />
              </Col>
              <Col flex="1">
                <Outlet />
              </Col>
            </Row>
          </Layout>
        )}
        {pathname !== "/scan" && <Outlet />}
      </div>
    </>
  );
};

export default LayoutApp;
