import React, { useState } from "react";
import { Table, Input, Typography, Flex, Dropdown, Button, Menu } from "antd";
import { FaSearch } from "react-icons/fa";
import { ColumnType } from "antd/lib/table";
import { MenuProps } from "antd/lib";

interface BrowserTableProps {
  displayData: {
    data: {
      columns: string[];
      results: any[];
    };
  };
}

interface Counts {
  [key: string]: { [key: string]: number };
}

const BrowserTable: React.FC<BrowserTableProps> = ({ displayData }) => {
  const columns = displayData?.data?.columns || [];
  const results = displayData?.data?.results || [];

  const [searchText, setSearchText] = useState<string | RegExp>("");

  const getColumnSearchProps = (): ColumnType<any> => ({
    filterIcon: (filtered) => (
      <FaSearch style={{ color: filtered ? "#1890ff" : undefined }} />
    ),
    render: (text: string) => {
      if (!searchText) {
        return text;
      }
      try {
        const regex = new RegExp(`(${searchText})`, "gi");
        const parts = text.toString();
        return regex.test(parts) ? (
          <Typography.Text mark>{parts}</Typography.Text>
        ) : (
          parts
        );
      } catch (e) {
        return text;
      }
    },
  });

  const renderCustomTableColumn = (column: string): ColumnType<any> => ({
    dataIndex: column.toLowerCase(),
    title: column,
    key: column.toLowerCase(),
    sorter: (a, b) =>
      (a[column.toLowerCase()] || "").localeCompare(
        b[column.toLowerCase()] || ""
      ),
    ...getColumnSearchProps(),
  });

  const renderCustomTableData = (data: any[]): any[] => {
    const counts: Counts = {};

    return data.map((row) => {
      const obj: { [key: string]: any } = {};
      columns.forEach((column, index) => {
        obj[column.toLowerCase()] = row[index];

        // Count duplicates
        if (!counts[column]) {
          counts[column] = {};
        }

        if (counts[column][row[index]]) {
          counts[column][row[index]] += 1;
        } else {
          counts[column][row[index]] = 1;
        }
      });

      return { ...obj, counts };
    });
  };

  const regexes = [
    {
      name: "IP Address",
      regex: `^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$`,
    },
    {
      name: "Email Address",
      regex: "^([a-z0-9_\\.\\+-]+)@([\\da-z\\.-]+)\\.([a-z\\.]{2,6})$",
    },
    {
      name: "IPv6 Address",
      regex:
        "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))",
    },
    {
      name: "International Phone Number",
      regex:
        "^(?:(?:\\(?(?:00|\\+)([1-4]\\d\\d|[1-9]\\d?)\\)?)?[\\-\\.\\ \\\\/]?)?((?:\\(?\\d{1,}\\)?[\\-\\.\\ \\\\/]?){0,})(?:[\\-\\.\\ \\\\/]?(?:#|ext\\.?|extension|x)[\\-\\.\\ \\\\/]?(\\d+))?$",
    },
    {
      name: "File Path",
      regex:
        "((\\/|\\|\\/\\/|https?:\\\\|https?:\\/\\/)[a-z0-9_@\\-^!#$%&+={}.\\/\\\\[\\]]+)+\\.[a-z]+$",
    },
  ];

  const items = (
    <Menu>
      {regexes.map((regex) => (
        <Menu.Item
          key={regex.name}
          onClick={() => {
            console.log(regex.regex);
            setSearchText(regex.regex);
          }}
        >
          {regex.name}
        </Menu.Item>
      ))}
    </Menu>
  );

  return (
    <>
      <Flex justify="space-between" className="mb-4">
        <Dropdown overlay={items} trigger={["click"]}>
          <Button type="text">Regexes</Button>
        </Dropdown>
        <Flex justify="space-between">
          <Input.Search
            placeholder="Search"
            allowClear
            onChange={(e) => setSearchText(e.target.value)}
            value={searchText}
            style={{ width: 350 }}
          />
        </Flex>
      </Flex>
      <Table
        dataSource={renderCustomTableData(results)}
        columns={columns.map((column) => renderCustomTableColumn(column))}
        pagination={true}
      />
    </>
  );
};

export default BrowserTable;
