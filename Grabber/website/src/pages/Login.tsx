import Link from "antd/es/typography/Link";
import { LoginUser } from "../service/api";
import { Button, Form, Input, Typography } from "antd";
import { Content } from "antd/es/layout/layout";

export const Login: React.FC = () => {
  const submit = async (values) => {
    const { email, password } = values;

    const resp = await LoginUser(email, password);
    if (resp.message === "success") {
      localStorage.setItem("token", resp.token);
      location.href = "/";
    } else {
      console.log("error");
    }
  };

  return (
    <Content style={{ padding: "20px" }}>
      <Typography.Title level={2}>Login</Typography.Title>
      <Form name="loginToUser" onFinish={submit} labelCol={{ span: 6 }}>
        <Form.Item
          name="email"
          label="Email"
          rules={[
            { required: true, message: "Please enter your email" },
            { type: "email", message: "Please enter a valid email address" },
          ]}
        >
          <Input type="Email" placeholder="Email" />
        </Form.Item>

        <Form.Item
          name="password"
          label="Password"
          rules={[{ required: true, message: "Please enter your password" }]}
        >
          <Input.Password placeholder="Password" />
        </Form.Item>
        <Form.Item wrapperCol={{ offset: 6 }}>
          <Button type="primary" htmlType="submit">
            Login
          </Button>
        </Form.Item>
        <Typography.Text>
          Don't have an account? <Link href="/register">Register</Link>
        </Typography.Text>
      </Form>
    </Content>
  );
};
