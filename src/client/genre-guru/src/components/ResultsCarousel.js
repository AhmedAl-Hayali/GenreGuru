import React, { useState } from 'react';
import PlayCard from './PlayCard';
import '../styles/carousel.css';

const ResultsCarousel = ({ results }) => {
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
        <PlayCard 
          key={index} 
          track={track} 
          onPlay={handlePlay}
          isPlaying={track.id === currentTrackId} 
        />
      ))}
    </div>
  );
};

export default ResultsCarousel;
