import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import navigation
import '../styles/playcard.css';
import { FaPlay, FaStop } from 'react-icons/fa';
import { fetchRecommendations } from "../services/backend_api";
import { getDeezerPreview } from "../services/api";
import { getDeezerTrackFromISRC } from "../services/api";



const PlayCard = ({ track, onPlay, isPlaying, variant = "search", isSelected = false }) => {
  const { name, artists, album, preview_url, external_ids} = track;
  const artistNames = artists.map(artist => artist.name).join(', ');
  const [audio, setAudio] = useState(null);
  const navigate = useNavigate(); // Initialize navigation

  const handlePlayClick = async (e) => {
    e.stopPropagation(); // Prevent triggering the card click event

    if (isPlaying) {
      if (audio) {
        audio.pause();
        audio.currentTime = 0;
        setAudio(null);
        onPlay(null, null);
      }
      return;
    }

    let trackUrl = preview_url;
    if (!trackUrl) {
      console.log("Fetching Deezer preview...");
      trackUrl = await getDeezerPreview(external_ids?.isrc);
    }

    if (trackUrl) {
      const newAudio = new Audio(trackUrl);
      newAudio.play();
      setAudio(newAudio);
      onPlay(newAudio, track.id);

      newAudio.onended = () => {
        setAudio(null);
        onPlay(null, null);
      };
    } else {
      alert('Preview not available for this track.');
    }
  };

  // Handle clicking on the playcard itself
  const handleCardClick = async () => {
    try {
      const isrc = track?.external_ids.isrc;
      if (!isrc) throw new Error("No ISRC available for this track");
  
      const deezerTrack = await getDeezerTrackFromISRC(isrc);
      if (!deezerTrack) throw new Error("Failed to get Deezer track");
  
      const trackIds = await fetchRecommendations(deezerTrack); // pass full object
  
      navigate("/results", {
        state: { trackIds },
      });
    } catch (error) {
      console.error("Error handling card click:", error);
    }
  };

  useEffect(() => {
    return () => {
      if (audio) {
        audio.pause();
        audio.currentTime = 0;
      }
    };
  }, [audio]);
  
  return (
    <div 
      className={`play-card ${variant === "recommendation" ? "recommendation-card" : ""} ${isSelected ? "selected" : ""}`} 
    >

      <img className="album-art" src={album.images[0]?.url || ''} alt={name} />
      <div className="track-info">
        <div className="track-name">{name}</div>
        <div className="artist-name">{artistNames}</div>
      </div>
      <button className="play-btn" onClick={handlePlayClick}>
        {isPlaying ? <FaStop size={18} /> : <FaPlay size={18} />}
      </button>
    </div>
  );
};

export default PlayCard;
