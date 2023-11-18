import React, { useEffect, useMemo, useState } from "react";
import { Card, List, Input, Select, Space, Tooltip } from "antd";
import {
  SearchOutlined,
  SortAscendingOutlined,
  SortDescendingOutlined,
} from "@ant-design/icons";
import { getScanNetworkType } from "../../service/api";
import { useLocation } from "react-router-dom";

const { Option } = Select;

type NetworkActivityProps = {
  type: string;
};

const NetworkActivityType: React.FC<NetworkActivityProps> = ({ type }) => {
  const [data, setData] = useState<string[]>([]);
  const [searchText, setSearchText] = useState("");
  const [filterKey, setFilterKey] = useState("all");
  const [sortOrder, setSortOrder] = useState<"ascend" | "descend" | null>(null);

  useMemo(() => {
    if (searchText === "") return;
    setFilterKey("all");
  }, [searchText]);

  useMemo(() => {
    if (filterKey === "all") return;
    setSearchText("");
  }, [filterKey]);

  useMemo(() => {
    if (sortOrder === null) return;
    setFilterKey("all");
    setSearchText("");
  }, [sortOrder]);

  const sortedData =
    data.length > 0
      ? data.sort((a, b) => {
          if (sortOrder === "ascend") return a.localeCompare(b);
          if (sortOrder === "descend") return b.localeCompare(a);
          return 0;
        })
      : [];

  const handleSearch = (value: string) => {
    setSearchText(value);
  };

  const handleFilterChange = (value: string) => {
    setFilterKey(value);
  };

  const handleSortChange = () => {
    setSortOrder((prev) => (prev === "ascend" ? "descend" : "ascend"));
  };

  const pathname = useLocation();

  useEffect(() => {
    const getData = async () => {
      const name = new URLSearchParams(pathname.search).get("id");
      const data = await getScanNetworkType(name || "", type);
      setData(data);
    };

    getData();
  }, []);

  return (
    <Card title={`${type.toUpperCase()} Requests`} className="my-4">
      <Space direction="vertical" style={{ width: "100%" }}>
        <Input
          prefix={<SearchOutlined />}
          placeholder="Search"
          value={searchText}
          onChange={(e) => handleSearch(e.target.value)}
        />
        <Select
          placeholder="Filter by"
          onChange={handleFilterChange}
          value={filterKey}
        >
          <Option value="all">All</Option>
          <Option value="PA">PA</Option>
          {/* Add more filter options as needed */}
        </Select>
        <Tooltip title="Sort">
          <span onClick={handleSortChange}>
            {sortOrder === "ascend" ? (
              <SortAscendingOutlined />
            ) : (
              <SortDescendingOutlined />
            )}
          </span>
        </Tooltip>
      </Space>

      <List
        size="large"
        bordered
        dataSource={sortedData}
        renderItem={(item) => <List.Item>{item}</List.Item>}
      />
    </Card>
  );
};

export default NetworkActivityType;
