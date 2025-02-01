import React, { useState } from 'react';
import { FaSearch, FaUpload } from 'react-icons/fa'; // Import icons
import '../styles/components.css';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSearch = () => {
    if (query.trim() !== '') {
      onSearch(query);
    }
  };

  return (
    <div className="search-container">
      <div className="search-bar">
        <FaSearch className="search-icon" />
        <input
          type="text"
          placeholder="Search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button className="upload-btn">
          <FaUpload /> Upload
        </button>
      </div>
    </div>
  );
};

export default SearchBar;
