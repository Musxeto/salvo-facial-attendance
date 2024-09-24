import React, { useState, useEffect } from "react";
import axios from "axios";
import logo from "../assets/salvo.png";
import AttendanceTable from "./AttendanceTable";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { AiOutlineReload } from "react-icons/ai";
import Navbar from "./Navbar";

const api = "http://127.0.0.1:8001";

const HomePage = () => {
  const [records, setRecords] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalContent, setModalContent] = useState({});
  const [lastLog, setLastLog] = useState({});
  const [selectedTab, setSelectedTab] = useState("live");

  useEffect(() => {
    if (selectedTab === "live") {
      fetchTodayLogs();
      fetchLastLog();
      const intervalId = setInterval(() => {
        fetchLastLog();
      }, 2000);

      return () => clearInterval(intervalId);
    }
  }, [selectedTab, lastLog]);

  const fetchTodayLogs = async () => {
    try {
      console.log(`${api}/today_logs/`)
      const response = await axios.get(`${api}/today_logs/`);
      setRecords(response.data);
    } catch (error) {
      console.error("Error fetching today logs:", error);
      toast.error("Error fetching today logs");
    }
  };

  const fetchLastLog = async () => {
    try {
      const response = await axios.get(`${api}/last_log/`);
      const newLog = response.data;
      if (
        lastLog.employee_id !== newLog.employee_id ||
        lastLog.log_time !== newLog.log_time
      ) {
        setLastLog(newLog);
        setModalContent(newLog);
        setIsModalOpen(true);
      }
    } catch (error) {
      console.error("Error fetching last log:", error);
    }
  };

  const handleReload = () => {
    fetchTodayLogs();
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-gray-50">
     
      {/* Header */}
      <header className="bg-caribbean-current text-white w-full py-6 text-center">
        <img
          src={logo}
          alt="Company Logo"
          className="w-20 h-auto mx-auto mb-4"
        />
        <h1 className="text-4xl font-bold">Salvo Attendance System</h1>
      </header>

      <main className="flex flex-col items-center w-full px-4 py-8">
        <div className="w-full max-w-5xl bg-white shadow-lg rounded-lg overflow-hidden">
          {/* Tabs */}
          <div className="flex justify-between items-center px-4 py-2 bg-prussian-blue text-white">
            <div className="flex space-x-4">
              <button
                onClick={() => setSelectedTab("live")}
                className={`py-2 px-6 ${
                  selectedTab === "live"
                    ? "bg-caribbean-current"
                    : "bg-prussian-blue"
                } hover:bg-keppel rounded-lg transition-all duration-300`}
              >
                Live
              </button>
              <button
                onClick={() => setSelectedTab("table")}
                className={`py-2 px-6 ${
                  selectedTab === "table"
                    ? "bg-caribbean-current"
                    : "bg-prussian-blue"
                } hover:bg-keppel rounded-lg transition-all duration-300`}
              >
                Table
              </button>
            </div>

            {/* Reload button for Table */}
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

          {/* Tab content */}
          {selectedTab === "live" && (
            <div className="w-full p-6">
              <h2 className="text-2xl text-center font-semibold text-prussian-blue">
                Live Attendance Log
              </h2>
              {/* Modal for new attendance log */}
              {isModalOpen && (
                <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
                  <div className="bg-white p-10 rounded-lg shadow-lg w-full max-w-3xl">
                    <h2 className="text-3xl font-bold mb-6 text-center">
                      New Attendance Log
                    </h2>
                    <div className="grid grid-cols-2 gap-8">
                      <div className="flex justify-center">
                        <img
                          src={`${api}${modalContent.employee_image}`}
                          alt="Employee"
                          className="w-72 h-72 object-cover rounded-lg"
                        />
                      </div>
                      <div className="space-y-4">
                        <p className="text-xl">
                          <strong>Employee ID:</strong>{" "}
                          {modalContent.employee_id}
                        </p>
                        <p className="text-xl">
                          <strong>Log Time:</strong> {modalContent.log_time}
                        </p>
                        <p className="text-xl">
                          <strong>Employee Name:</strong>{" "}
                          {modalContent.employee_name}
                        </p>
                      </div>
                    </div>
                    <div className="flex justify-center mt-8">
                      <button
                        onClick={() => setIsModalOpen(false)}
                        className="bg-caribbean-current text-white py-3 px-8 rounded hover:bg-keppel transition-all duration-300"
                      >
                        Close
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {selectedTab === "table" && (
            <div className="w-full p-6">
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
