import React, { useState } from "react";
import Signup from "./SignUp";
import { toast, ToastContainer } from "react-toastify";

const Dashboard = () => {
  const [isAdmin, setIsAdmin] = useState(false); // To check if the user confirms they are an admin
  const [password, setPassword] = useState(""); // To store the admin password input
  const [isAuthenticated, setIsAuthenticated] = useState(false); // To check if the admin password is correct

  const adminPassword = "admin123"; // Replace with your real admin password (or fetch from the backend securely)

  // Function to handle admin authentication
  const handleLogin = (e) => {
    e.preventDefault();
    if (password === adminPassword) {
      setIsAuthenticated(true);
    } else {
      toast.error("Incorrect admin password!");
    }
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
      {isAuthenticated && <Signup />}
    </div>
  );
};

export default Dashboard;
