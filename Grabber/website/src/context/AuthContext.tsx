import { createContext, useContext, useState } from "react";
import { currentUser, verifyToken } from "../service/api";

// Create a new context
type AuthContextType = {
  isLoggedIn: boolean;
  userDetails: any;
  checkToken: () => void;
  isLoading: boolean;
};

const AuthContext = createContext({} as AuthContextType);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userDetails, setUserDetails] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // You can define functions to update the state here if needed

  const checkToken = () => {
    setIsLoading(true);
    const token = localStorage.getItem("token");

    verifyToken(token!)
      .then((data) => {
        if (!data) return;
        if (data.message === "success") {
          console.log("Logged in");
          setIsLoggedIn(true);

          // get user details
          const getUserDetails = async () => {
            await currentUser().then((data) => {
              console.log(data);
              if (!data.data) return;
              if (data.message === "success") {
                setUserDetails(data.data);
              }
            });
          };
          getUserDetails();
        } else {
          localStorage.removeItem("token");
          setIsLoggedIn(false);
          if (
            window.location.pathname !== "/login" &&
            window.location.pathname !== "/register"
          ) {
            window.location.href = "/login";
          }
        }
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  // Provide the context values to the components
  const contextValue = {
    isLoggedIn,
    userDetails,
    checkToken,
    isLoading,
  };

  console.log(userDetails);

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
