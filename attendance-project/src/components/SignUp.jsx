import React, { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import {
  FaUser,
  FaEnvelope,
  FaLock,
  FaPhone,
  FaAddressCard,
  FaUpload,
  FaSpinner,
  FaCalendar,
  FaDollarSign,
  FaUserShield,
  FaToggleOn,
  FaToggleOff,
} from "react-icons/fa";
import { Link, useNavigate } from "react-router-dom";
import { Line } from "rc-progress";
import axios from "axios";

const Signup = () => {
  const [formData, setFormData] = useState({
    first_name: "",
    middle_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
    phone: "",
    alternate_phone: "",
    address: "",
    date_of_birth: "",
    employment_date: "",
    department: "",
    position: "",
    salary: "",
    manager: "",
    emergency_contact: "",
    profile_image: null,
    imagePreview: null,
    is_staff: false,
    is_active: true,
    is_hr_manager: false,
  });

  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  let navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setFormData({
      ...formData,
      profile_image: file,
      imagePreview: URL.createObjectURL(file),
    });
  };

  const handleNextStep = () => {
    if (validateStep(step)) {
      setStep(step + 1);
    } else {
      toast.error("Please fill in all required fields");
    }
  };

  const handlePreviousStep = () => {
    setStep(step - 1);
  };

  const validateStep = (currentStep) => {
    switch (currentStep) {
      case 1:
        return formData.first_name && formData.last_name && formData.username;
      case 2:
        return formData.email && formData.password;
      case 3:
        return formData.phone && formData.address;
      case 4:
        return (
          formData.date_of_birth && formData.department && formData.position
        );
      case 5:
        return true; // Always validate for the last step
      default:
        return true;
    }
  };

  const handleSignup = (e) => {
    e.preventDefault();
    setLoading(true);

    const formDataObj = new FormData();
    Object.keys(formData).forEach((key) => {
      if (formData[key] !== null) {
        formDataObj.append(key, formData[key]);
      }
    });
    console.log(formData);
    axios
      .post("http://localhost:8000/api/employees/", formDataObj, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        toast.success("Signed Up Successfully");
        setFormData({
          first_name: "",
          middle_name: "",
          last_name: "",
          username: "",
          email: "",
          password: "",
          phone: "",
          alternate_phone: "",
          address: "",
          date_of_birth: "",
          employment_date: "",
          department: "",
          position: "",
          salary: "",
          manager: "",
          emergency_contact: "",
          profile_image: null,
          imagePreview: null,
          is_staff: false,
          is_active: true,
          is_hr_manager: false,
        });
        setStep(1);
        toast.success("Successfully Signed Up");
      })
      .catch((error) => {
        toast.error("An error occurred. Please try again.");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const getProgress = () => (step / 6) * 100;

  return (
    <div className="w-full max-w-md">
      <h2 className="text-3xl mb-6 text-black text-center">Employee Signup</h2>
      <Line percent={getProgress()} strokeWidth="2" strokeColor="black" />
      <form
        onSubmit={handleSignup}
        className="bg-white text-black p-8 rounded-lg shadow-2xl"
      >
        {/* Step 1 */}
        {step === 1 && (
          <>
            <div className="mb-4">
              <label className="block text-sm mb-2">First Name</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaUser className="m-2" />
                <input
                  type="text"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Middle Name</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaUser className="m-2" />
                <input
                  type="text"
                  name="middle_name"
                  value={formData.middle_name}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                />
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Last Name</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaUser className="m-2" />
                <input
                  type="text"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Username</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaUser className="m-2" />
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>
            </div>
            <div className="flex justify-between">
              <button
                type="button"
                onClick={handleNextStep}
                className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
              >
                Next
              </button>
            </div>
          </>
        )}

        {/* Step 2 */}
        {step === 2 && (
          <>
            <div className="mb-4">
              <label className="block text-sm mb-2">Email</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaEnvelope className="m-2" />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Password</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaLock className="m-2" />
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>
            </div>
            <div className="flex justify-between">
              <button
                type="button"
                onClick={handlePreviousStep}
                className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
              >
                Previous
              </button>
              <button
                type="button"
                onClick={handleNextStep}
                className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
              >
                Next
              </button>
            </div>
          </>
        )}

        {/* Step 3 */}
        {step === 3 && (
          <>
            <div className="mb-4">
              <label className="block text-sm mb-2">Phone</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaPhone className="m-2" />
                <input
                  type="text"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Alternate Phone</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaPhone className="m-2" />
                <input
                  type="text"
                  name="alternate_phone"
                  value={formData.alternate_phone}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                />
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Address</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaAddressCard className="m-2" />
                <input
                  type="text"
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>
            </div>
            <div className="flex justify-between">
              <button
                type="button"
                onClick={handlePreviousStep}
                className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
              >
                Previous
              </button>
              <button
                type="button"
                onClick={handleNextStep}
                className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
              >
                Next
              </button>
            </div>
          </>
        )}

        {/* Step 4 */}
        {step === 4 && (
          <>
            <div className="mb-4">
              <label className="block text-sm mb-2">Date of Birth</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaCalendar className="m-2" />
                <input
                  type="date"
                  name="date_of_birth"
                  value={formData.date_of_birth}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Employment Date</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaCalendar className="m-2" />
                <input
                  type="date"
                  name="employment_date"
                  value={formData.employment_date}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Department</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaAddressCard className="m-2" />
                <input
                  type="text"
                  name="department"
                  value={formData.department}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Position</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaUserShield className="m-2" />
                <input
                  type="text"
                  name="position"
                  value={formData.position}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Salary</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaDollarSign className="m-2" />
                <input
                  type="text"
                  name="salary"
                  value={formData.salary}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Manager</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaUserShield className="m-2" />
                <input
                  type="text"
                  name="manager"
                  value={formData.manager}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                />
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Emergency Contact</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaPhone className="m-2" />
                <input
                  type="text"
                  name="emergency_contact"
                  value={formData.emergency_contact}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                />
              </div>
            </div>

            <div className="flex justify-between">
              <button
                type="button"
                onClick={handlePreviousStep}
                className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
              >
                Previous
              </button>
              <button
                type="button"
                onClick={handleNextStep}
                className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
              >
                Next
              </button>
            </div>
          </>
        )}
        {step == 5 && (
          <>
            <div className="mb-4">
              <label className="block text-sm mb-2">Profile Image</label>
              <input
                type="file"
                name="profile_image"
                accept="image/*"
                onChange={handleImageChange}
                className="w-full"
              />
              {formData.imagePreview && (
                <img
                  src={formData.imagePreview}
                  alt="Profile Preview"
                  className="w-32 h-32 object-cover mt-2 rounded"
                />
              )}
            </div>
            <div className="flex justify-between">
              <button
                type="button"
                onClick={handlePreviousStep}
                className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
              >
                Previous
              </button>
              <button
                type="button"
                onClick={handleNextStep}
                className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
              >
                Next
              </button>
            </div>
          </>
        )}
        {/* Step 5 */}
        {step === 6 && (
          <>
            <div className="mb-4">
              <label className="block text-sm mb-2">HR Manager</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaUserShield className="m-2" />
                <select
                  name="is_hr_manager"
                  value={formData.is_hr_manager}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                >
                  <option value={false}>False</option>
                  <option value={true}>True</option>
                </select>
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Manager</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaUserShield className="m-2" />
                <select
                  name="is_staff"
                  value={formData.is_staff}
                  onChange={handleInputChange}
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                >
                  <option value={false}>False</option>
                  <option value={true}>True</option>
                </select>
              </div>
            </div>
            <div className="mb-4">
              <label className="block text-sm mb-2">Active Status</label>
              <div className="flex items-center bg-gray-200 rounded">
                {formData.is_active ? (
                  <FaToggleOn className="m-2" />
                ) : (
                  <FaToggleOff className="m-2" />
                )}
                <input
                  type="checkbox"
                  name="is_active"
                  checked={formData.is_active}
                  onChange={handleInputChange}
                  className="ml-2"
                />
                <span className="ml-2">Active</span>
              </div>
            </div>
            <div className="flex justify-between">
              <button
                type="button"
                onClick={handlePreviousStep}
                className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
              >
                Previous
              </button>
              <button
                type="submit"
                className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
                disabled={loading}
              >
                {loading ? <FaSpinner className="animate-spin" /> : "Sign Up"}
              </button>
            </div>
          </>
        )}

        <ToastContainer />
      </form>
    </div>
  );
};

export default Signup;
