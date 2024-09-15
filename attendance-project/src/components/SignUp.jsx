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
    last_name: "",
    username: "",
    profile_image: null,
  });

  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  let navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
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
      case 3:
        console.log("nigga");
        return true;
      case 4:
        console.log("nigga");
        return true;
      case 5:
        return true;
      default:
        return true;
    }
  };

  const handleSignup = (e) => {
    e.preventDefault();
    setLoading(true);

    const formDataObj = new FormData();
    Object.keys(formData).forEach((key) => {
      let value = formData[key];
      formDataObj.append(key, value);
    });

    axios
      .post("http://localhost:8001/signup/", formDataObj, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        toast.success("Signup successful!");
        navigate("/login");
      })
      .catch((error) => {
        setLoading(false);
        toast.error("Signup failed.");
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

        {step == 2 && (
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
        {step === 3 && (
          <>
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
