import React, { useState, useEffect } from "react";
import axios from "axios";
import logo from "../assets/salvo.png";
import AttendanceTable from "./AttendanceTable";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { AiOutlineReload } from "react-icons/ai"; 

const api="http://localhost:8001"
const HomePage = () => {
  
  const [records, setRecords] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalContent, setModalContent] = useState({});
  const [lastLog, setLastLog] = useState({});
  const [ws, setWs] = useState(null);
  const [selectedTab, setSelectedTab] = useState("live"); // New state for tab selection

  useEffect(() => {
    if (selectedTab === "live") {
      fetchTodayLogs();
      fetchLastLog();
      const intervalId = setInterval(() => {
        fetchLastLog();
      }, 5000);

      return () => clearInterval(intervalId);
    }
  }, [selectedTab, lastLog]);

  const fetchTodayLogs = async () => {
    try {
      const response = await axios.get("http://localhost:8001/today_logs/");
      setRecords(response.data);
    } catch (error) {
      console.error("Error fetching today logs:", error);
      toast.error("Error fetching today logs");
    }
  };

  const fetchLastLog = async () => {
    try {
      const response = await axios.get("http://localhost:8001/last_log/");
      const newLog = response.data;

      // Check if the new log is different from the current one
      if (lastLog.employee_id !== newLog.employee_id || lastLog.log_time !== newLog.log_time) {
        setLastLog(newLog);
        setModalContent(newLog);
        console.log(`${api}${modalContent.employee_image}`)
        setIsModalOpen(true); // Only set to true if there's a new log
      } 
    } catch (error) {
      console.error("Error fetching last log:", error);
      toast.error("Error fetching last log");
    }
  };

  const handleReload = () => {
    fetchTodayLogs();
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-white">
      <header className="bg-caribbean-current text-white w-full py-4 text-center flex flex-col items-center">
        <img src={logo} alt="Company Logo" className="w-32 h-auto mb-2" />
        <h1 className="text-4xl font-bold">Salvo Attendance System</h1>
      </header>

      <main className="flex flex-col items-center w-full p-4">
        <div className="w-full max-w-4xl bg-white shadow-md rounded-lg overflow-hidden">
          <div className="flex justify-between items-center px-4 py-2 bg-prussian-blue text-white">
            <div className="flex space-x-4">
              <button
                onClick={() => setSelectedTab("live")}
                className={`py-2 px-4 ${selectedTab === "live" ? "bg-caribbean-current" : "bg-prussian-blue"} text-white rounded`}
              >
                Live
              </button>
              <button
                onClick={() => setSelectedTab("table")}
                className={`py-2 px-4 ${selectedTab === "table" ? "bg-caribbean-current" : "bg-prussian-blue"} text-white rounded`}
              >
                Table
              </button>
            </div>
            {selectedTab === "table" && (
              <button
                onClick={handleReload}
                className="text-white hover:text-gray-300"
                aria-label="Reload Data"
              >
                <AiOutlineReload size={24} />
              </button>
            )}
          </div>
          {selectedTab === "live" && (
            <div className="mt-8 w-full bg-white">
              <h2 className="text-xl font-semibold px-4 py-2 bg-prussian-blue text-white">Live Attendance Log</h2>
              {/* Add content for the Live tab */}
              {/* Display live logs or any other relevant data */}
              {isModalOpen && (
                <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
                  <div className="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full">
                    <h2 className="text-2xl font-bold mb-4">New Attendance Log</h2>
                    <img src={`${api}${modalContent.employee_image}`} />
                    <p>
                      <strong>Employee ID:</strong> {modalContent.employee_id}
                    </p>
                    <p>
                      <strong>Log Time:</strong> {modalContent.log_time}
                    </p>
                    <p>
                      <strong>Employee Name:</strong> {modalContent.employee_name}
                    </p>
                    <button
                      onClick={() => setIsModalOpen(false)}
                      className="mt-4 bg-caribbean-current text-white py-2 px-4 rounded hover:bg-teal-700"
                    >
                      Close
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}
          {selectedTab === "table" && (
            <div className="mt-8 w-full max-w-4xl bg-white shadow-md rounded-lg overflow-hidden">
              <AttendanceTable records={records} />
            </div>
          )}
        </div>

        <ToastContainer />
      </main>
    </div>
  );
};

export default HomePage;
