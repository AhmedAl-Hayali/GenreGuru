import React, { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/loading.css";
import { getDeezerTrackFromISRC } from "../services/api";
import { fetchRecommendations } from "../services/backend_api";

const LoadingPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { selectedTrack } = location.state || {};

  useEffect(() => {
    const getAndSendRecommendations = async () => {
      try {
        const isrc = selectedTrack?.external_ids?.isrc;
        if (!isrc) throw new Error("No ISRC available");

        console.log("ISRC:", isrc);

        const deezerTrack = await getDeezerTrackFromISRC(isrc);
        console.log("Deezer Track:", deezerTrack);

        if (!deezerTrack) throw new Error("Could not fetch Deezer track");

        const recommendedTrackIds = await fetchRecommendations(deezerTrack);
        console.log("Recommended Track IDs:", recommendedTrackIds);

        navigate("/results", {
          state: { trackIds: recommendedTrackIds, selectedTrack },
        });
      } catch (err) {
        console.error("Error fetching recommendations:", err);
        alert("Error getting recommendations.");
      }
    };

    getAndSendRecommendations();
  }, [selectedTrack, navigate]);

  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>Getting your recommendations...</p>
    </div>
  );
};

export default LoadingPage;
