import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import PlayCard from "../components/PlayCard";
import "../styles/results.css";
import { getSpotifyTrackFromISRC } from "../services/api";

const ResultsPage = () => {
  const location = useLocation();
  const { deezerTrackIds } = location.state || {};
  const [recommendations, setRecommendations] = useState([]);
  const [playingTrack, setPlayingTrack] = useState(null);

  useEffect(() => {
    const fetchSpotifyTracks = async () => {
      if (!deezerTrackIds || deezerTrackIds.length === 0) return;

      try {
        const promises = deezerTrackIds.map(async (id) => {
          const deezerTrack = await getDeezerTrackFromID(id);
          const isrc = deezerTrack?.isrc;
          if (!isrc) return null;
          return await getSpotifyTrackFromISRC(isrc);
        });

        const resolvedTracks = await Promise.all(promises);
        const filteredTracks = resolvedTracks.filter((track) => track !== null);
        setRecommendations(filteredTracks);
      } catch (err) {
        console.error("Error fetching Spotify tracks:", err);
      }
    };

    fetchSpotifyTracks();
  }, [deezerTrackIds]);

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