import React from 'react';
import SearchBar from '../components/SearchBar';
import '../styles/components.css';

const HomePage = () => {
  return (
    <div className="home-container">
      <h1 className="main-title">GenreGuru</h1>
      <SearchBar />
    </div>
  );
};

export default HomePage;
