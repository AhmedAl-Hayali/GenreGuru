import React, { useState } from 'react';
import PlayCard from './PlayCard';
import '../styles/carousel.css';

const ResultsCarousel = ({ results, selectedTrack, onTrackClick }) => {
  const [currentAudio, setCurrentAudio] = useState(null);
  const [currentTrackId, setCurrentTrackId] = useState(null);

  const handlePlay = (audio, trackId) => {
    if (currentAudio) {
      currentAudio.pause(); // Stop the currently playing track
    }
    setCurrentAudio(audio);
    setCurrentTrackId(trackId);
  };

  return (
    <div className="results-carousel">
      {results.map((track, index) => (
        <div
          key={index}
          className={`carousel-item ${selectedTrack?.id === track.id ? 'selected' : ''}`}
          onClick={() => onTrackClick(track)}
        >
          <PlayCard 
            track={track} 
            onPlay={handlePlay}
            isPlaying={track.id === currentTrackId}
            isSelected={selectedTrack?.id === track.id}
          />

        </div>
      ))}
    </div>
  );
};

export default ResultsCarousel;
