import { Content } from "antd/es/layout/layout";
import { RegisterUser } from "../service/api";
import { Button, Form, Input, Typography } from "antd";

export const Register: React.FC = () => {
  const submit = async (values) => {
    const { name, email, password } = values;

    const resp = await RegisterUser(name, password, email);
    if (resp.message === "success") {
      location.href = "/login";
    } else {
      console.log("error");
    }
  };

  return (
    <Content style={{ padding: "20px" }}>
      <Typography.Title level={2}>Register</Typography.Title>
      <Form name="registerUser" onFinish={submit} labelCol={{ span: 6 }}>
        <Form.Item
          name="name"
          label="Name"
          rules={[{ required: true, message: "Please enter your name" }]}
        >
          <Input type="text" placeholder="Name" />
        </Form.Item>

        <Form.Item
          name="email"
          label="Email"
          rules={[
            { required: true, message: "Please enter your email" },
            { type: "email", message: "Please enter a valid email address" },
          ]}
        >
          <Input type="email" placeholder="Email" />
        </Form.Item>

        <Form.Item
          name="password"
          label="Password"
          rules={[
            { required: true, message: "Please enter a password" },
            { min: 6, message: "Password must be at least 6 characters" },
          ]}
        >
          <Input.Password placeholder="Password" />
        </Form.Item>

        <Form.Item wrapperCol={{ offset: 6 }}>
          <Button type="primary" htmlType="submit" onClick={submit}>
            Register
          </Button>
        </Form.Item>
      </Form>
    </Content>
  );
};
