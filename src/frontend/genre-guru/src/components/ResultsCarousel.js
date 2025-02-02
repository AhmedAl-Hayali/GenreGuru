import React from 'react';
import '../styles/components.css';
import PlayCard from './PlayCard';

const ResultsCarousel = ({ results }) => {
  return (
    <div className="results-carousel">
      {results.map((track) => (
        <PlayCard key={track.id} track={track} />
      ))}
    </div>
  );
};

export default ResultsCarousel;
