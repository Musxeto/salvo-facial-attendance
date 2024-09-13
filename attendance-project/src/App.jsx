import React from "react";
import AllRoutes from "./routes/AllRoutes";
import "./index.css";
import Navbar from "./components/Navbar";
import { BrowserRouter } from "react-router-dom";

const App = () => (
  <BrowserRouter>
    <div className="App bg-prussian-blue">
      <Navbar />
      <AllRoutes />
    </div>
  </BrowserRouter>
);

export default App;
