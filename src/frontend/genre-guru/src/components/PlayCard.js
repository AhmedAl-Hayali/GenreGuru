import React from 'react';

const PlayCard = ({ song }) => (
  <div className="play-card">
    <img src={song.albumCover} alt="Album Cover" />
    <div className="song-info">
      <p>{song.name}</p>
      <p>{song.artist}</p>
    </div>
    <audio controls>
      <source src={song.snippet} type="audio/mpeg" />
      Your browser does not support the audio element.
    </audio>
  </div>
);

export default PlayCard;
