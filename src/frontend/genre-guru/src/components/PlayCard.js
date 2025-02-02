import React from 'react';
import { FaPlay } from 'react-icons/fa';

const PlayCard = ({ track }) => {
  const { name, artists, album, preview_url } = track;

  const handlePlayPreview = () => {
    if (!preview_url) return;
    const audio = new Audio(preview_url);
    audio.play();
  };

  return (
    <div className="play-card">
      <img className="album-art" src={album.images[0]?.url} alt="Album Art" />
      <div className="track-info">
        <p className="track-name">{name}</p>
        <p className="artist-name">{artists.map((artist) => artist.name).join(', ')}</p>
      </div>
      {preview_url && (
        <button className="play-btn" onClick={handlePlayPreview}>
          <FaPlay />
        </button>
      )}
    </div>
  );
};

export default PlayCard;
