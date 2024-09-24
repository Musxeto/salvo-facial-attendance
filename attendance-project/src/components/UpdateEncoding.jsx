import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { FaUser, FaArrowRight, FaTrash } from "react-icons/fa";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const UpdateEncoding = () => {
  const [formData, setFormData] = useState({
    employee_id: "",
    profile_images: [], // For multiple images
  });

  const [imagePreviews, setImagePreviews] = useState([]); // Previews for the selected images
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  const fileInputRef = useRef(null); // Ref to programmatically trigger file input

  // Fetch employees based on the search query
  useEffect(() => {
    if (searchQuery.length > 1) {
      axios
        .get(`http://localhost:8001/search_employee?query=${searchQuery}`)
        .then((response) => {
          setSearchResults(response.data);
        })
        .catch((error) => {
          console.error("Error fetching employee search results:", error);
        });
    } else {
      setSearchResults([]);
    }
  }, [searchQuery]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === "employee_id") {
      setSearchQuery(value);
    }
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleEmployeeSelect = (employee_id) => {
    setFormData({
      ...formData,
      employee_id,
    });
    setSearchResults([]); // Hide search results after selection
  };

  const handleNextStep = () => {
    if (formData.employee_id) {
      setStep(step + 1);
    } else {
      toast.error("Please select an employee.");
    }
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setFormData((prevState) => ({
      ...prevState,
      profile_images: [...prevState.profile_images, ...files], // Append new files
    }));

    // Create image previews
    const previews = files.map((file) => URL.createObjectURL(file));
    setImagePreviews((prevState) => [...prevState, ...previews]); // Append new previews
  };

  const handleRemoveImage = (index) => {
    setFormData((prevState) => {
      const newImages = [...prevState.profile_images];
      newImages.splice(index, 1); // Remove the image from the array
      return { ...prevState, profile_images: newImages };
    });
    setImagePreviews((prevState) => {
      const newPreviews = [...prevState];
      newPreviews.splice(index, 1); // Remove the preview
      return newPreviews;
    });
  };

  const handleUpdateEncoding = (e) => {
    e.preventDefault();
    setLoading(true);

    const formDataObj = new FormData();
    formDataObj.append("employee_id", formData.employee_id);

    // Append multiple images to FormData
    formData.profile_images.forEach((image) => {
      formDataObj.append(`profile_images`, image); 
    });

    axios
      .post("http://localhost:8001/update_encoding/", formDataObj, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((response) => {
        toast.success("Encoding updated successfully!");
        setLoading(false);
      })
      .catch((error) => {
        setLoading(false);
        toast.error("Failed to update encoding.");
      });
  };

  const handleAddMoreFiles = () => {
    fileInputRef.current.click(); // Trigger file input click programmatically
  };

  return (
    <div className="w-full max-w-md">
      <ToastContainer />
      <h2 className="text-3xl mb-6 text-black text-center">Update Encoding</h2>

      <form onSubmit={handleUpdateEncoding} className="bg-white p-8 rounded-lg shadow-2xl">
        {step === 1 && (
          <>
            <div className="mb-4">
              <label className="block text-sm mb-2">Search Employee</label>
              <div className="flex items-center bg-gray-200 rounded">
                <FaUser className="m-2" />
                <input
                  type="text"
                  name="employee_id"
                  value={formData.employee_id}
                  onChange={handleInputChange}
                  placeholder="Enter ID, username, first or last name"
                  className="w-full p-2 bg-gray-200 border-none outline-none"
                  required
                />
              </div>

              {/* Search Results Dropdown */}
              {searchResults.length > 0 && (
                <ul className="bg-white border border-gray-300 mt-2 rounded-md shadow-md max-h-40 overflow-auto">
                  {searchResults.map((employee) => (
                    <li
                      key={employee.employee_id}
                      className="p-2 hover:bg-gray-100 cursor-pointer"
                      onClick={() => handleEmployeeSelect(employee.employee_id)}
                    >
                      {employee.first_name} {employee.last_name} ({employee.username})
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <button
              type="button"
              onClick={handleNextStep}
              className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
            >
              Next <FaArrowRight className="ml-2" />
            </button>
          </>
        )}

        {/* Step 2: Upload Profile Image */}
        {step === 2 && (
          <>
            <div className="mb-4">
              <label className="block text-sm mb-2">Profile Images</label>
              <input
                ref={fileInputRef}
                type="file"
                name="profile_images"
                accept="image/*"
                multiple // Allow multiple image selection
                onChange={handleFileChange}
                className="w-full p-2 bg-gray-200 border-none outline-none hidden" // Hide the input
              />

              {/* Button to trigger file input */}
              <button
                type="button"
                onClick={handleAddMoreFiles}
                className="bg-gray-500 text-white p-2 rounded hover:bg-gray-600 transition duration-200"
              >
                Add More Files
              </button>
            </div>

            {/* Preview Selected Images */}
            {imagePreviews.length > 0 && (
              <div className="mb-4 grid grid-cols-2 gap-2">
                {imagePreviews.map((preview, index) => (
                  <div className="relative" key={index}>
                    <img
                      src={preview}
                      alt={`Selected image ${index + 1}`}
                      className="w-full h-32 object-cover rounded-lg" // Consistent height
                    />
                    <button
                      type="button"
                      className="absolute top-0 right-0 bg-red-500 text-white rounded-full p-1 m-1"
                      onClick={() => handleRemoveImage(index)}
                    >
                      <FaTrash />
                    </button>
                  </div>
                ))}
              </div>
            )}

            <button
              type="submit"
              className="bg-black text-white p-2 rounded hover:bg-gray-800 transition duration-200"
            >
              Submit
            </button>
          </>
        )}
      </form>
    </div>
  );
};

export default UpdateEncoding;
