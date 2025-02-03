import React, { useRef } from "react";
import { FaUpload } from "react-icons/fa";
import "../styles/uploadfile.css";

const UploadFile = ({ onFileUpload }) => {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log("Uploaded file:", file);
      alert(`File "${file.name}" selected successfully!`);
      if (onFileUpload) {
        onFileUpload(file);
      } else {
        console.error("onFileUpload function is missing!");
      }
    }
  };

  return (
    <div className="upload-wrapper">
      <input
        type="file"
        accept=".wav"
        ref={fileInputRef}
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
      <button className="upload-btn" onClick={() => fileInputRef.current.click()}>
        <FaUpload /> Upload
      </button>
    </div>
  );
};

export default UploadFile;
