import React, { useState } from 'react';

const Item = ({ item, onUpdateItem, onDeleteItem, isHighlighted }) => {
  const [rating, setRating] = useState(item.rating);

  const handleRatingChange = (newRating) => {
    setRating(newRating);
    onUpdateItem({ ...item, rating: newRating });
  };

  const itemStyle = {
    backgroundImage: `url(${item.cover})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
  };

  return (
    <div className={`item ${isHighlighted ? 'highlighted' : ''}`} style={itemStyle}>
      <button className="delete-button" onClick={() => onDeleteItem(item.id)}>X</button>
      <div className="item-content">
        <div className="item-details">
          <h3>{item.title}</h3>
          <p>{item.artist}</p>
          <p id="year">{item.year}</p>
        </div>
        <div className="item-rating">
          {[...Array(7)].map((star, index) => (
            <button
              key={index}
              className={index < rating ? 'star on' : 'star off'}
              onClick={() => handleRatingChange(index + 1)}
            >
              &#9733;
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Item;
