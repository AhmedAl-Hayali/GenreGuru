import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import PlayCard from "../components/PlayCard";
import { fetchTrackDetails } from "../services/api"; // Use centralized API logic
import "../styles/results.css";

const ResultsPage = () => {
  const location = useLocation();
  const { spotifyIds } = location.state || {};
  const [recommendations, setRecommendations] = useState([]);
  const [playingTrack, setPlayingTrack] = useState(null);

  useEffect(() => {
    if (spotifyIds && spotifyIds.length > 0) {
      const getRecommendations = async () => {
        try {
          const tracks = await fetchTrackDetails(spotifyIds);
          setRecommendations(tracks);
        } catch (error) {
          console.error("Failed to load recommendations:", error);
        }
      };

      getRecommendations();
    }
  }, [spotifyIds]);

  // Handle play/stop logic
  const handlePlay = (audio, trackId) => {
    if (playingTrack && playingTrack.audio) {
      playingTrack.audio.pause();
      playingTrack.audio.currentTime = 0; // Reset previous audio
    }

    if (audio) {
      audio.play();
      setPlayingTrack({ audio, trackId });
    } else {
      setPlayingTrack(null);
    }
  };

  return (
    <div className="results-container">
      <h2>Recommended Songs</h2>
      <div className="results-list">
        {recommendations.map((track) => (
          <PlayCard
            key={track.id}
            track={track}
            isPlaying={playingTrack?.trackId === track.id}
            onPlay={handlePlay}
            variant="recommendation"
          />
        ))}
      </div>
    </div>
  );
};

export default ResultsPage;
