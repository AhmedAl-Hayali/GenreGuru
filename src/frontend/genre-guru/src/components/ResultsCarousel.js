import React from 'react';
import PlayCard from './PlayCard';

const ResultsCarousel = ({ songs }) => (
  <div className="results-carousel">
    {songs.map((song, index) => (
      <PlayCard key={index} song={song} />
    ))}
  </div>
);

export default ResultsCarousel;
