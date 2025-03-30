import { FaUpload } from "react-icons/fa";
import "../styles/uploadfile.css";
import { uploadWavFile } from "../services/backend_api";
import { useNavigate } from "react-router-dom";
import React, { useRef, useState } from "react";

const MAX_SIZE_MB = 20;

const UploadFile = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file || file.type !== "audio/wav") {
      alert("Please upload a valid .wav file.");
      return;
    }

    const fileSizeMB = file.size / (1024 * 1024);
    if (fileSizeMB > MAX_SIZE_MB) {
      alert("File too large. Please upload a file under 20MB.");
      return;
    }

    try {
      setUploading(true);

      const formData = new FormData();
      formData.append("file", file);

      const deezerTracks = await uploadWavFile(formData);
      navigate("/results", { state: { deezerTracks } });
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Error uploading audio file.");
    } finally {
      setUploading(false);
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
      <button className="upload-btn" onClick={() => fileInputRef.current.click()} disabled={uploading}>
        {uploading ? "Uploading..." : <><FaUpload /> Upload</>}
      </button>
    </div>
  );
};

export default UploadFile;
