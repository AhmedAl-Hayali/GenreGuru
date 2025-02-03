import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import navigation
import '../styles/playcard.css';
import axios from 'axios';
import { FaPlay, FaStop } from 'react-icons/fa';

const PlayCard = ({ track, onPlay, isPlaying, variant = "search" }) => {
  const { name, artists, album, preview_url, external_ids, id } = track;
  const artistNames = artists.map(artist => artist.name).join(', ');
  const [audio, setAudio] = useState(null);
  const navigate = useNavigate(); // Initialize navigation

  const fetchItunesPreview = async (isrc) => {
    try {
      const response = await axios.get(`https://itunes.apple.com/search`, {
        params: { term: name, media: 'music', entity: 'musicTrack', limit: 1 }
      });

      if (response.data.results.length > 0) {
        return response.data.results[0].previewUrl;
      }
    } catch (error) {
      console.error("iTunes API fetch failed:", error);
    }
    return null;
  };

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
      trackUrl = await fetchItunesPreview(external_ids?.isrc);
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
  const handleCardClick = () => {
    navigate(`/results/${id}`); // Navigate to the results page with track ID
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
