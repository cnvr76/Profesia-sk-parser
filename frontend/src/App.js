import React, { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import "./App.css";

import VacanciesPage from "./pages/VacanciesPage";
import HomePage from "./pages/HomePage";

const App = () => {
  const [cursorPos, setCursorPos] = useState({ x: 0, y: 0 });
  useEffect(() => {
    const handleMouseMove = (e) => {
      setCursorPos({
        x: e.clientX,
        y: e.clientY,
      });
    };
    return () => window.addEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<HomePage />} /> */}

        <Route path="/" element={<VacanciesPage />} />

        <Route path="/home" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

export default App;
