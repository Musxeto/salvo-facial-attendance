import React, { useState, useEffect } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import logo from "../assets/salvo.png";
import AttendanceTable from "./AttendanceTable"; 

const HomePage = () => {
  const [status, setStatus] = useState("");
  const [employee, setEmployee] = useState(null);
  const [records, setRecords] = useState([]);

  useEffect(() => {
    const fetchRecords = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/attendance/records"
        );
        setRecords(response.data.attendance);
      } catch (error) {
        console.error("Error fetching attendance records:", error);
      }
    };

    fetchRecords();
  }, []);

  return (
    <div className="flex flex-col items-center min-h-screen bg-white">
      <header className="bg-caribbean-current text-white w-full py-4 text-center flex flex-col items-center">
        <img src={logo} alt="Company Logo" className="w-32 h-auto mb-2" />
        <h1 className="text-4xl font-bold">Salvo Attendance System</h1>
      </header>
      <main className="flex flex-col items-center w-full p-4">
        {status && <p className="mt-2 text-lg">{status}</p>}
        {employee && (
          <div className="mt-4 p-4 bg-keppel text-white rounded shadow-lg">
            <h2 className="text-xl font-semibold">Employee Info</h2>
            <img
              src={employee.photo}
              alt="Employee"
              className="w-24 h-24 rounded-full mt-2"
            />
            <p className="mt-2">Name: {employee.name}</p>
            <p>Employee ID: {employee.id}</p>
            <p>Time In: {employee.time_in}</p>
            <p>Time Out: {employee.time_out}</p>
          </div>
        )}
        <div className="mt-8 w-full max-w-4xl bg-white shadow-md rounded-lg overflow-hidden">
          <h2 className="text-xl font-semibold text-center py-4 bg-prussian-blue text-white">
            Attendance Table
          </h2>
          <AttendanceTable records={records} />
        </div>
      </main>
      <ToastContainer />
    </div>
  );
};

export default HomePage;
