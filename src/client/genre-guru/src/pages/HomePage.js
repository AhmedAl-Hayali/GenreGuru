import React, { useState } from "react";
import SearchBar from "../components/SearchBar";
import ResultsCarousel from "../components/ResultsCarousel";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [selectedTrack, setSelectedTrack] = useState(null);
  const navigate = useNavigate();

  const handleSearchResults = (results) => {
    setSearchResults(results);
    setSelectedTrack(null); // Clear selection on new search
  };

  const handleFileUpload = (file) => {
    console.log("File uploaded in HomePage:", file);
  };

  const handleTrackClick = (track) => {
    if (selectedTrack?.id === track.id) {
      navigate("/loading", { state: { selectedTrack: track } });
    } else {
      setSelectedTrack(track);
    }
  };
  

  return (
    <div className="home-container">
      <h1 className="main-title">GenreGuru</h1>
      <SearchBar onSearchResults={handleSearchResults} onFileUpload={handleFileUpload} />
      {searchResults.length > 0 && (
        <ResultsCarousel
          results={searchResults}
          selectedTrack={selectedTrack}
          onTrackClick={handleTrackClick}
        />
      )}
    </div>
  );
};



export default HomePage;
