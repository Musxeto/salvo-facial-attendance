import React, { useState } from "react";
import Signup from "./SignUp";
import { toast, ToastContainer } from "react-toastify";
import UpdateEncoding from "./UpdateEncoding";

const Dashboard = () => {
  const [isAdmin, setIsAdmin] = useState(false);
  const [password, setPassword] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [selectedTab, setSelectedTab] = useState("signup");
  const [userExists, setUserExists] = useState(false); 

  const adminPassword = "admin123";
  
  const handleLogin = (e) => {
    e.preventDefault();
    if (password === adminPassword) {
      setIsAuthenticated(true);
      setUserExists(false);
    } else {
      toast.error("Incorrect admin password!");
    }
  };

  const handleTabChange = (tab) => {
    setSelectedTab(tab);
  };

  return (
    <div className="flex flex-col justify-center items-center min-h-screen bg-gray-100">
      {/* Ask if the user is an admin */}
      {!isAdmin && !isAuthenticated && (
        <div className="mb-4">
          <p className="text-lg font-bold mb-2">Are you an admin?</p>
          <button
            onClick={() => setIsAdmin(true)}
            className="bg-caribbean-current text-white px-4 py-2 rounded"
          >
            Yes, I am an admin
          </button>
        </div>
      )}

      {/* If the user confirms they are an admin, ask for the admin password */}
      {isAdmin && !isAuthenticated && (
        <form onSubmit={handleLogin} className="flex flex-col items-center">
          <p className="text-lg font-bold mb-2">Enter Admin Password</p>
          <input
            type="password"
            placeholder="Admin Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border border-gray-300 rounded p-2 mb-4"
            required
          />
          <button
            type="submit"
            className="bg-caribbean-current text-white px-4 py-2 rounded"
          >
            Submit
          </button>
        </form>
      )}

      <ToastContainer />

      {isAuthenticated && (
        <div className="w-full max-w-md">
          <div className="flex justify-between mb-4">
            <button
              onClick={() => handleTabChange("signup")}
              className={`px-4 py-2 rounded ${
                selectedTab === "signup"
                  ? "bg-black text-white"
                  : "bg-gray-300 text-black"
              }`}
            >
              Sign Up
            </button>
            <button
              onClick={() => handleTabChange("update")}
              className={`px-4 py-2 rounded ${
                selectedTab === "update"
                  ? "bg-black text-white"
                  : "bg-gray-300 text-black"
              }`}
            >
              Update Encoding
            </button>
          </div>

          {selectedTab === "signup" && <Signup />}
          {selectedTab === "update" && <UpdateEncoding />}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
