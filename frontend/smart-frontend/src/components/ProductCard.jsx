// src/components/ProductCard.jsx
import React from "react";
import "./ProductCard.css";

const ProductCard = ({ product }) => {
  // Handle different data structures for books vs other products
  const title = product.title || product.name || "Unknown Product";
  const price = product.price || 0;
  const rating = product.rating || 0;
  const image = product.image || "https://via.placeholder.com/150";
  
  // For books, show author instead of description
  const isBook = product.author && !product.description;
  const displayText = isBook ? product.author : (product.description?.substring(0, 100) || "No description available");

  return (
    <div className="card">
      <img src={image} alt={title} />
      <div className="details">
        <h3>{title}</h3>
        <p>{displayText}{!isBook && product.description && product.description.length > 100 ? "..." : ""}</p>
        {price > 0 && <p><strong>₹{price}</strong></p>}
        {rating > 0 && <p>⭐ {rating}</p>}
      </div>
    </div>
  );
};

export default ProductCard;
