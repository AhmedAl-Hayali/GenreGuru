import React from 'react';

const UploadFile = ({ onFileSelected }) => {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log("File selected in UploadFile component:", file);
      onFileSelected(file); // Pass the file to SearchBar.js
    }
  };

  return (
    <input
      type="file"
      accept=".wav"
      id="hidden-file-input"
      style={{ display: 'none' }}
      onChange={handleFileChange}
    />
  );
};

export default UploadFile;
