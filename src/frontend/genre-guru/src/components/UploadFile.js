import React, { useRef } from "react";
import { FaUpload } from "react-icons/fa";

const UploadFile = ({ onFileUpload }) => {
  const fileInputRef = useRef(null); // Hidden file input reference

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log("Uploaded file:", file);
      alert(`File "${file.name}" selected successfully!`);
      onFileUpload(file);
    }
  };

  const triggerFileSelect = () => {
    fileInputRef.current.click();
  };

  return (
    <div>
      <input
        type="file"
        accept=".wav"
        ref={fileInputRef}
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
      <button className="upload-btn" onClick={triggerFileSelect}>
        <FaUpload /> Upload
      </button>
    </div>
  );
};

export default UploadFile;
