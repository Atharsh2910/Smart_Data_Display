// src/components/FilterBar.jsx
import React from "react";
import "./FilterBar.css";

const FilterBar = ({ category, setCategory, setSearch, setSort }) => {
  return (
    <div className="filter-bar">
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="books">Books</option>
        <option value="electronics">Electronics</option>
        <option value="personal_health">Personal Health</option>
      </select>

      <input
        type="text"
        placeholder="Search by name..."
        onChange={(e) => setSearch(e.target.value)}
      />

      <select onChange={(e) => setSort(e.target.value)}>
        <option value="">Sort</option>
        <option value="price_asc">Price ↑</option>
        <option value="price_desc">Price ↓</option>
        <option value="rating_desc">Rating ↓</option>
      </select>
    </div>
  );
};

export default FilterBar;
