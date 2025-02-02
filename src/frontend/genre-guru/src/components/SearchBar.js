import React, { useState, useRef } from 'react';
import { FaSearch, FaUpload } from 'react-icons/fa';
import '../styles/searchbar.css';
import { searchSong } from '../services/api';

const SearchBar = ({ onSearchResults, onFileUpload }) => {
  const [query, setQuery] = useState('');
  const fileInputRef = useRef(null);

  // Handle search query submission
  const handleSearch = async () => {
    if (query.trim() !== '') {
      try {
        const results = await searchSong(query);
        console.log("Search Results:", results);
        onSearchResults(results); // Pass search results to parent
      } catch (error) {
        console.error("Search failed:", error);
      }
    }
  };

  // Handle file selection for upload
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log("Uploaded file:", file);
      alert(`File "${file.name}" selected successfully!`);
      onFileUpload(file);
    }
  };

  // Trigger file input
  const triggerFileSelect = () => {
    fileInputRef.current.click();
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
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
        />
        <input
          type="file"
          accept=".wav"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
        <button className="upload-btn" onClick={triggerFileSelect}>
          <FaUpload /> Upload
        </button>
      </div>
    </div>
  );
};

export default SearchBar;
