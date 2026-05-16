import React from 'react';
import './RecommendationCard.css';

const RecommendationCard = ({ title, type }) => {
  return (
    <div className="recommendation-card">
      <div className="recommendation-card-content">
        <h3 className="recommendation-title">{title}</h3>
        <p className="recommendation-type">{type}</p>
      </div>
    </div>
  );
};

export default RecommendationCard;