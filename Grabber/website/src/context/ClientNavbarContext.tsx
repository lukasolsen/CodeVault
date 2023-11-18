import { createContext, useContext, useState } from "react";

type ClientNavbarContextType = {
  collapsed: boolean;
  selectedKey: string;
  toggleCollapsed: () => void;
  setSelectedKey: React.Dispatch<React.SetStateAction<string>>;
};

const ClientNavbarContext = createContext({} as ClientNavbarContextType);

export function ClientNavbarProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [collapsed, setCollapsed] = useState(false);
  const [selectedKey, setSelectedKey] = useState("overview");

  const toggleCollapsed = () => {
    setCollapsed(!collapsed);
  };

  const contextValue = {
    collapsed,
    selectedKey,
    toggleCollapsed,
    setSelectedKey,
  };

  return (
    <ClientNavbarContext.Provider value={contextValue}>
      {children}
    </ClientNavbarContext.Provider>
  );
}

export function useClientNavbar() {
  return useContext(ClientNavbarContext);
}
