import React, { useState } from "react";
import SearchBar from "../components/SearchBar";
import ResultsCarousel from "../components/ResultsCarousel";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

const HomePage = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [selectedTrack, setSelectedTrack] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSearchResults = (results) => {
    setSearchResults(results);
    setSelectedTrack(null); // Clear selection on new search
  };

  const handleFileUpload = (file) => {
    console.log("File uploaded in HomePage:", file);
  };

  const handleTrackClick = (track) => {
    if (loading) return;

    if (selectedTrack?.id === track.id) {
      setLoading(true);
      navigate("/loading", { state: { selectedTrack: track } });
    } else {
      setSelectedTrack(track);
    }
  };

  return (
    <motion.div
      className="home-container"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
    >
      <h1 className="main-title">GenreGuru</h1>
      <SearchBar
        onSearchResults={handleSearchResults}
        onFileUpload={handleFileUpload}
      />
      {searchResults.length > 0 && (
        <ResultsCarousel
          results={searchResults}
          selectedTrack={selectedTrack}
          onTrackClick={handleTrackClick}
        />
      )}
    </motion.div>
  );
};

export default HomePage;
