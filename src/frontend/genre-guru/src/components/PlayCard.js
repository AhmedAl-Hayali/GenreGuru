import React from 'react';
import '../styles/playcard.css';

const PlayCard = ({ track }) => {
  const { name, artists, album, preview_url } = track;
  const artistNames = artists.map(artist => artist.name).join(', ');

  const handlePlayClick = () => {
    if (preview_url) {
      new Audio(preview_url).play();
    } else {
      alert('Preview not available for this track.');
    }
  };

  return (
    <div className="play-card">
      <img className="album-art" src={album.images[0]?.url || ''} alt={name} />
      <div className="track-info">
        <div className="track-name">{name}</div>
        <div className="artist-name">{artistNames}</div>
      </div>
      <button className="play-btn" onClick={handlePlayClick}>▶</button>
    </div>
  );
};

export default PlayCard;
