//const mainUri = "https://grabbed.onrender.com";
const mainUri = "http://localhost:8080";

const getScans = async () => {
  const response = await fetch(`${mainUri}/api/v2/scan/scans`, {
    method: "GET",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("token") || "",
    },
  });

  if (response.ok) {
    const users = await response.json();
    console.log(users);
    return users.data;
  } else {
    throw new Error("Request failed with status: " + response.status);
  }
};

const getScan = async (id: string) => {
  const response = await fetch(`${mainUri}/api/v2/scan/scan/${id}`, {
    method: "GET",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("token") || "",
    },
  });

  if (response.ok) {
    const user = await response.json();

    return user.data;
  }
};

const getScanWebsitesPre = async (id: string) => {
  const response = await fetch(
    `${mainUri}/api/v2/scan/scan/${id}/attacks/browsers/pre`,
    {
      method: "GET",
      headers: {
        // "Content-Type" header is removed for GET requests
        Authorization: "Bearer " + localStorage.getItem("token") || "",
      },
    }
  );

  if (response.ok) {
    const websites = await response.json();
    return websites.data;
  }
};

const getScanWebsiteType = async (
  id: string,
  browser: string,
  type: string
) => {
  const response = await fetch(
    `${mainUri}/api/v2/scan/scan/${id}/attacks/browser/${browser}/${type}`,
    {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token") || "",
      },
    }
  );

  if (response.ok) {
    const websites = await response.json();
    return websites.data;
  }
};

const getScanNetworkOverview = async (id: string) => {
  const response = await fetch(
    `${mainUri}/api/v2/scan/scan/${id}/attacks/network/overview`,
    {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token") || "",
      },
    }
  );

  if (response.ok) {
    const websites = await response.json();
    return websites.data;
  }
};

const getScanNetworkType = async (id: string, type: string) => {
  const response = await fetch(
    `${mainUri}/api/v2/scan/scan/${id}/attacks/network/${type}`,
    {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token") || "",
      },
    }
  );

  if (response.ok) {
    const websites = await response.json();
    return websites.data;
  }
};

const getScanDiscord = async (id: string) => {
  const response = await fetch(
    `${mainUri}/api/v2/scan/scan/${id}/attacks/discord/overview`,
    {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token") || "",
        AllowOrigin: "*",
      },
    }
  );

  if (response.ok) {
    const websites = await response.json();
    return websites.data;
  }
};

const RegisterUser = async (name: string, password: string, email: string) => {
  const response = await fetch(`${mainUri}/api/v2/user/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: name,
      password: password,
      email: email,
    }),
  });

  const data = await response.json();
  return data;
};

const LoginUser = async (email: string, password: string) => {
  const response = await fetch(`${mainUri}/api/v2/user/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email,
      password: password,
    }),
  });

  const data = await response.json();
  return data;
};

const RegisterClient = async (
  name: string,
  password: string,
  email: string,
  company: string,
  bio: string
) => {
  const response = await fetch(`${mainUri}/api/v2/client/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + localStorage.getItem("token") || "",
    },
    body: JSON.stringify({
      name: name,
      password: password,
      email: email,
      company: company,
      bio: bio,
    }),
  });

  const data = await response.json();
  return data;
};

export const verifyToken = async (token: string) => {
  const response = await fetch(`${mainUri}/api/v2/user/verify-token`, {
    method: "POST",
    headers: {
      Authorization: "Bearer " + token,
    },
  });

  const data = await response.json();
  return data;
};

export const currentUser = async () => {
  const token = localStorage.getItem("token");
  const response = await fetch(`${mainUri}/api/v2/user/current_user`, {
    method: "GET",
    headers: {
      Authorization: "Bearer " + token,
    },
  });

  const data = await response.json();
  return data;
};

export {
  getScans,
  getScan,
  getScanWebsitesPre,
  getScanWebsiteType,
  RegisterUser,
  LoginUser,
  RegisterClient,
  getScanNetworkOverview,
  getScanNetworkType,
  getScanDiscord,
};
