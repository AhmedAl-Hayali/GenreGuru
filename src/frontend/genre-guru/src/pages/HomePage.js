import React, { useState } from "react";
import SearchBar from "../components/SearchBar";
import ResultsCarousel from "../components/ResultsCarousel";

const HomePage = () => {
  const [searchResults, setSearchResults] = useState([]);

  const handleSearchResults = (results) => {
    setSearchResults(results);
  };

  return (
    <div className="home-container">
      <h1 className="main-title">GenreGuru</h1>
      <SearchBar onSearchResults={handleSearchResults} />
      {searchResults.length > 0 && <ResultsCarousel results={searchResults} />}
    </div>
  );
};

export default HomePage;
