import React from "react";
import { Layout, Typography, Form, Input, Button, Select } from "antd";
import { RegisterClient } from "../service/api";

const { Content } = Layout;
const { Title } = Typography;
const { Option } = Select;

const AddClient: React.FC = () => {
  const onFinish = async (values: any) => {
    const { name, email, password, company, bio } = values;
    // Handle form submission here
    await RegisterClient(name, password, email, company, bio)
      .then((response) => {
        if (response.message === "success") {
          location.href = "/client?id=" + response.data.id;
        } else {
          console.log("error", response.error);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <Content style={{ padding: "20px" }}>
      <Title level={2}>Add Client</Title>
      <Form name="addClientForm" onFinish={onFinish} labelCol={{ span: 6 }}>
        <Form.Item
          name="name"
          label="Name"
          rules={[
            { required: true, message: "Please enter the client's name" },
          ]}
        >
          <Input placeholder="Enter name" />
        </Form.Item>
        <Form.Item
          name="email"
          label="Email"
          rules={[
            { required: true, message: "Please enter the client's email" },
            { type: "email", message: "Please enter a valid email address" },
          ]}
        >
          <Input placeholder="Enter email" />
        </Form.Item>
        <Form.Item
          name="password"
          label="Password"
          rules={[
            { required: true, message: "Please enter a password" },
            { min: 6, message: "Password must be at least 6 characters" },
          ]}
        >
          <Input.Password placeholder="Enter password" />
        </Form.Item>
        <Form.Item
          name="company"
          label="Company"
          rules={[{ required: true, message: "Please select a company" }]}
        >
          <Select placeholder="Select a company">
            <Option value="Company A">Company A</Option>
            <Option value="Company B">Company B</Option>
            <Option value="Company C">Company C</Option>
            {/* Add more company options here */}
          </Select>
        </Form.Item>
        <Form.Item name="bio" label="Bio">
          <Input.TextArea placeholder="Enter bio" />
        </Form.Item>
        <Form.Item wrapperCol={{ offset: 6 }}>
          <Button type="primary" htmlType="submit">
            Add Client
          </Button>
        </Form.Item>
      </Form>
    </Content>
  );
};

export default AddClient;
