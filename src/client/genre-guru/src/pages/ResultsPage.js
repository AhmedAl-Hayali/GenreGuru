import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import PlayCard from "../components/PlayCard";
import ResultsCarousel from "../components/ResultsCarousel";
import "../styles/results.css";
import { getSpotifyTrackFromISRC, getDeezerTrackFromID } from "../services/api";
import { motion } from "framer-motion";

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { trackIds, selectedTrack } = location.state || {};

  const [recommendations, setRecommendations] = useState([]);
  const [playingTrack, setPlayingTrack] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSpotifyTracks = async () => {
      if (!trackIds || trackIds.length === 0) return;

      try {
        setLoading(true);

        const promises = trackIds.map(async (id) => {
          try {
            const deezerTrack = await getDeezerTrackFromID(id);
            if (!deezerTrack || !deezerTrack.isrc) return null;

            const spotifyTrack = await getSpotifyTrackFromISRC(deezerTrack.isrc);
            return spotifyTrack?.id ? spotifyTrack : null;
          } catch (err) {
            return null;
          }
        });

        const resolvedTracks = await Promise.all(promises);
        const filteredTracks = resolvedTracks.filter((track) => track && track.id);

        // ✅ Track which trackIds failed
        const missingIds = trackIds.filter((_, idx) => !resolvedTracks[idx] || !resolvedTracks[idx]?.id);

        console.log("Filtered Tracks:", filteredTracks);
        if (missingIds.length > 0) {
          console.warn("❌ These track IDs failed to resolve:", missingIds);
        }

        setRecommendations(filteredTracks);
      } catch (err) {
        console.error("Error fetching Spotify tracks:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchSpotifyTracks();
  }, [trackIds]);

  const handlePlay = (audio, trackId) => {
    if (playingTrack?.audio) {
      playingTrack.audio.pause();
      playingTrack.audio.currentTime = 0;
    }

    if (audio) {
      audio.play();
      setPlayingTrack({ audio, trackId });
    } else {
      setPlayingTrack(null);
    }
  };

  return (
    <motion.div
      className="results-container"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
    >
      <h2>Recommended Songs</h2>

      {loading ? (
        <p>Loading recommendations...</p>
      ) : recommendations.length === 0 ? (
        <p>No recommendations found.</p>
      ) : (
        <ResultsCarousel
          results={recommendations}
          selectedTrack={selectedTrack}
          onTrackClick={() => {}}
        />
      )}

      <button onClick={() => navigate("/")} className="back-btn">
        ← Back
      </button>
    </motion.div>
  );
};

export default ResultsPage;
