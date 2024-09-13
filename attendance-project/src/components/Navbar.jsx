import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../assets/salvo.png'; // Ensure the correct path for the logo

const Navbar = () => {
  return (
    <nav className="bg-caribbean-current w-full px-6 py-4 text-white shadow-md">
      <div className="flex items-center justify-between">
        {/* Logo */}
        <Link to="/">
          <img src={logo} alt="Company Logo" className="w-12 h-auto" />
        </Link>

        {/* Navigation Links */}
        <ul className="flex space-x-8  justify-between">
          <li>
            <Link to="/" className="text-lg font-semibold hover:text-keppel transition-colors duration-300">
              Home
            </Link>
          </li>
          <li>
            <Link to="/dashboard" className="text-lg font-semibold hover:text-keppel transition-colors duration-300">
              Dashboard
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
