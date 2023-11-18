import { useEffect, useState } from "react";
import { RiArchive2Fill, RiDownload2Line } from "react-icons/ri";
import { getScans } from "./service/api";

type User = {
  id: number;
  bio: string;
  company: string;
  email: string;
  name: string;
  role: string;
};

function App() {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    // Add example user
    getScans().then((clients) => {
      console.log(clients);
      setUsers(clients);
    });
  }, []);

  return (
    <div className="min-h-screen p-6 text-gray-800">
      <section className="mt-8">
        {users.length === 0 ? (
          <div className="text-center flex flex-col justify-center items-center">
            <h2 className="text-2xl dark:text-white text-gray-800">
              No users found
            </h2>
            <p className="mt-2">
              <span className="dark:text-gray-400 text-gray-700">
                Please download the client from the link below:
              </span>
            </p>
            <a
              href="https://github.com/lukasolsen/The-Joy-of-Prankreation"
              className="text-blue-600 hover:underline dark:text-blue-400"
              target="_blank"
              rel="noopener noreferrer"
            >
              <span className="text-lg flex items-center gap-2">
                <RiDownload2Line className="inline-block align-middle" />{" "}
                Download the Client
              </span>
            </a>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {users.map((user: User, index) => (
              <div
                key={index}
                className="bg-white dark:bg-slate-800 rounded-md p-4 shadow-md dark:text-white text-gray-800"
              >
                <h2 className="text-2xl font-bold mb-2">{user.name}</h2>
                <p className="text-gray-600 dark:text-gray-400">
                  <span className="font-bold">
                    Timestamp: {new Date().toUTCString()}
                  </span>
                </p>
                <div className="flex flex-row items-center justify-between mt-4">
                  <button className="px-2 py-1 rounded-lg flex items-center gap-2 bg-red-600 text-white hover:bg-red-700">
                    <RiDownload2Line className="inline-block align-middle" />{" "}
                    Download
                  </button>

                  <a
                    className="px-2 py-1 rounded-lg flex items-center gap-2 bg-blue-600 text-white hover:bg-blue-700 cursor-pointer"
                    href={"/client?id=" + user.id}
                  >
                    <RiArchive2Fill className="inline-block align-middle" />
                    Discover
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
