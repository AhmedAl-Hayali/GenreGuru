import React, { useState } from "react";
import { FaSearch } from "react-icons/fa";
import "../styles/searchbar.css";
import { searchSong } from "../services/api";
import UploadFile from "./UploadFile";  

const SearchBar = ({ onSearchResults, onFileUpload }) => { 
  const [query, setQuery] = useState("");

  const handleSearch = async () => {
    if (query.trim() === "") return;
    try {
      const results = await searchSong(query);
      onSearchResults(results);
    } catch (error) {
      console.error("Search failed:", error);
    }
  };

  return (
    <div className="search-container">
      <div className="search-bar">
        <FaSearch className="search-icon" onClick={handleSearch} />
        <input
          type="text"
          placeholder="Search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSearch()}
        />

        <UploadFile onFileUpload={onFileUpload} />
      </div>
    </div>
  );
};

export default SearchBar;
