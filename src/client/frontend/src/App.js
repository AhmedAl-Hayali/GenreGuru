import React from 'react';
import HomePage from './pages/HomePage';
import ResultsPage from "./pages/ResultsPage";
import './styles/App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/results/:id" element={<ResultsPage />} />
      </Routes>
    </Router>
  );
};

export default App;
