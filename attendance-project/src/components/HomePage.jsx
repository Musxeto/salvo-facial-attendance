import React, { useState, useEffect } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import logo from "../assets/salvo.png";
import AttendanceTable from "./AttendanceTable";
import EmployeeModal from "./EmployeeModal";

const HomePage = () => {
  const [employee, setEmployee] = useState(null);
  const [isFirstLogin, setIsFirstLogin] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [records, setRecords] = useState([]);

  useEffect(() => {
    const fetchEmployee = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/employee");
        setEmployee(response.data.employee);
        setIsFirstLogin(response.data.isFirstLogin);
        setIsModalOpen(true); // Open modal when employee is fetched
      } catch (error) {
        console.error("Error fetching employee data:", error);
      }
    };

    fetchEmployee();
  }, []);

  return (
    <div className="flex flex-col items-center min-h-screen bg-white">
      <header className="bg-caribbean-current text-white w-full py-4 text-center flex flex-col items-center">
        <img src={logo} alt="Company Logo" className="w-32 h-auto mb-2" />
        <h1 className="text-4xl font-bold">Salvo Attendance System</h1>
      </header>

      <main className="flex flex-col items-center w-full p-4">
        {/* Attendance Table remains visible */}
        <div className="mt-8 w-full max-w-4xl bg-white shadow-md rounded-lg overflow-hidden">
          <h2 className="text-xl font-semibold text-center py-4 bg-prussian-blue text-white">
            Attendance Table
          </h2>
          <AttendanceTable records={records} />
        </div>

        {/* Employee Info Modal */}
        {employee && (
          <EmployeeModal
            employee={employee}
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
            isFirstLogin={isFirstLogin}
          />
        )}

        <ToastContainer />
      </main>
    </div>
  );
};

export default HomePage;
