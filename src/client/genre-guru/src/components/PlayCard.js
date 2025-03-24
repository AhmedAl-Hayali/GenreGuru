import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import navigation
import '../styles/playcard.css';
import { FaPlay, FaStop } from 'react-icons/fa';
import { fetchRecommendations } from "../services/local_api";
import { getDeezerPreview } from "../services/api";


const PlayCard = ({ track, onPlay, isPlaying, variant = "search" }) => {
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
      console.log("Fetching iTunes preview...");
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
      console.log("Sending Spotify ID:", track.id);
      const spotifyIds = await fetchRecommendations(track.id);
      navigate(`/results`, { state: { spotifyIds } });
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
  };

  return (
    <div 
      className={`play-card ${variant === "recommendation" ? "recommendation-card" : ""}`} 
      onClick={handleCardClick} // Navigate when clicking the card
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
