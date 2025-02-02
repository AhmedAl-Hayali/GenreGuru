import React from 'react';
import PlayCard from './PlayCard';
import '../styles/carousel.css';

const ResultsCarousel = ({ results }) => {
  return (
    <div className="results-carousel">
      {results.map((track, index) => (
        <PlayCard key={index} track={track} />
      ))}
    </div>
  );
};

export default ResultsCarousel;
