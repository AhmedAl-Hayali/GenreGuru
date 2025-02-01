import React from 'react';
import SearchBar from '../components/SearchBar';
import '../styles/components.css';

const HomePage = () => {
  
  const handleUpload = async (file) => {
    if (!file) {
      alert("No file selected.");
      return;
    }

    console.log("Uploading file:", file);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const data = await response.json();
      console.log("Upload successful:", data);
      alert("File uploaded successfully!");

    } catch (error) {
      console.error("Upload error:", error);
      alert(`Failed to upload file: ${error.message}`);
    }
  };

  return (
    <div className="home-container">
      <h1 className="main-title">GenreGuru</h1>
      <SearchBar onUpload={handleUpload} />
    </div>
  );
};

export default HomePage;
