import React, { useState } from "react";
import SearchBar from "../components/SearchBar";
import ResultsCarousel from "../components/ResultsCarousel";

const HomePage = () => {
  const [searchResults, setSearchResults] = useState([]);

  // Function to handle search results
  const handleSearchResults = (results) => {
    setSearchResults(results);
  };

  // Function to handle file uploads
  const handleFileUpload = (file) => {
    console.log("File uploaded in HomePage:", file);
  };

  return (
    <div className="home-container">
      <h1 className="main-title">GenreGuru</h1>
      <SearchBar onSearchResults={handleSearchResults} onFileUpload={handleFileUpload} />
      {searchResults.length > 0 && <ResultsCarousel results={searchResults} />}
    </div>
  );
};

export default HomePage;
