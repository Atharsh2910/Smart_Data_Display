// src/components/Hero.jsx
import React from "react";
import books from "../assets/books.jpg";
import electronics from "../assets/electronics.jpg";
import personal from "../assets/personal.jpg";
import "./Hero.css";

const Hero = ({ onCategorySelect }) => {
  return (
    <div className="hero-container">
      <h2 className="hero-title">Discover & Compare Smart Products</h2>
      <p className="hero-description">Explore all Books, Electronics and Personal Care products at a single place with ease</p>
      <div className="hero-images">
        <img
          src={books}
          alt="Books"
          className="hero-image hero-image-clickable"
          onClick={() => onCategorySelect("books")}
        />
        <img
          src={electronics}
          alt="Electronics"
          className="hero-image hero-image-clickable"
          onClick={() => onCategorySelect("electronics")}
        />
        <img
          src={personal}
          alt="Personal Care"
          className="hero-image hero-image-clickable"
          onClick={() => onCategorySelect("personal_health")}
        />
      </div>
      <button className="hero-button" onClick={() => onCategorySelect("books")}>Start Browsing</button>
    </div>
  );
};

export default Hero;
