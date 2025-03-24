import { FaUpload } from "react-icons/fa";
import "../styles/uploadfile.css";
import { uploadWavFile } from "../services/local_api";
import { useNavigate } from "react-router-dom";
import React, { useRef } from "react";

const UploadFile = ({ onFileUpload }) => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log("Uploaded file:", file);
      alert(`File "${file.name}" selected successfully!`);

      try {
        const spotifyIds = await uploadWavFile(file);
        navigate(`/results`, { state: { spotifyIds } });
      } catch (error) {
        console.error("Failed to process file:", error);
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
