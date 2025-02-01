import React, { useState, useRef } from 'react';
import { FaSearch, FaUpload } from 'react-icons/fa';
import '../styles/components.css';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null); // Reference to hidden file input

  const handleSearch = () => {
    if (query.trim() !== '') {
      onSearch(query);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      console.log("Uploaded file:", file);
      alert(`File "${file.name}" selected successfully!`);
    }
  };

  const triggerFileSelect = () => {
    fileInputRef.current.click(); // Opens file selector when Upload button is clicked
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
