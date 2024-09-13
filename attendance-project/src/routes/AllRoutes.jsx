import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from '../components/HomePage';
import Dashboard from '../components/Dashboard';

const AllRoutes = () => (
 
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path='/dashboard' element={<Dashboard />} />
    </Routes>

);

export default AllRoutes;
