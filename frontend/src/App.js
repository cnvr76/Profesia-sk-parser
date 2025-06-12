import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import "./App.css";

import VacanciesPage from "./pages/VacanciesPage";
import HomePage from "./pages/HomePage";

function App() {
  return (
    <Router>
      <Routes>
        {/* <Route path="/" element={<HomePage />} /> */}

        <Route path="/" element={<VacanciesPage />} />

        <Route path="/home" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
