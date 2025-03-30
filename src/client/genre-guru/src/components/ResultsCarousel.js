import React, { useState } from 'react';
import PlayCard from './PlayCard';
import '../styles/carousel.css';
import { motion } from "framer-motion";

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
      {results.map((track, index) => {
        if (!track || !track.id) return null; // ✅ safety check

        return (
          <motion.div
            key={track.id}
            className="carousel-item"
            onClick={() => onTrackClick(track)}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.05 }}
          >
            <PlayCard 
              track={track} 
              onPlay={handlePlay}
              isPlaying={track.id === currentTrackId}
              isSelected={selectedTrack?.id === track.id}
            />
          </motion.div>
        );
      })}
    </div>
  );
};

export default ResultsCarousel;
