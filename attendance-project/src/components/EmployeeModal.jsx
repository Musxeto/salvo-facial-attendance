import React, { useEffect } from "react";

const EmployeeModal = ({ employee, isOpen, onClose, isFirstLogin }) => {
  useEffect(() => {
    if (isOpen) {
      const timer = setTimeout(() => {
        onClose();
      }, 60000); 

      return () => clearTimeout(timer);
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white w-full max-w-lg p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold text-prussian-blue mb-4">Employee Info</h2>
        <div className="flex items-center">
          <img
            src={employee.photo_url}
            alt="Employee"
            className="w-24 h-24 rounded-full border-2 border-turquoise mr-4"
          />
          <div>
            <h2 className="text-xl font-semibold">{employee.name}</h2>
            <p className="text-gray-600">Department: {employee.department}</p>
            <p className="text-gray-600">Position: {employee.position}</p>
          </div>
        </div>
        <div className="mt-4 text-turquoise font-bold text-xl">
          {isFirstLogin ? "Welcome! This is your first login today." : "Welcome back!"}
        </div>
        <div className="mt-6 p-4 bg-caribbean-current text-white rounded-lg text-center">
          <p className="text-lg">
            Status: {employee.status === "in" ? "Clocked In" : "Clocked Out"}
          </p>
          <p>Time In: {employee.time_in || "N/A"}</p>
          <p>Time Out: {employee.time_out || "N/A"}</p>
        </div>
        <button
          className="mt-6 bg-prussian-blue text-white py-2 px-4 rounded hover:bg-turquoise"
          onClick={onClose}
        >
          Close
        </button>
      </div>
    </div>
  );
};


export default EmployeeModal;