import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import ProductCard from "./components/ProductCard";
import FilterBar from "./components/FilterBar";
import ChatbotBox from "./components/ChatbotBox";
import Hero from "./components/Hero";
import "./App.css";

function App() {
  const [category, setCategory] = useState("books");
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState("");
  const [showChatbot, setShowChatbot] = useState(false);

  const API_BASE = "http://localhost:10000/api/products";

  const fetchProducts = useCallback(async () => {
    try {
      const res = await axios.get(API_BASE, {
        params: { category, search, sort },
      });
      if (Array.isArray(res.data)) {
        setProducts(res.data);
      } else {
        setProducts([]);
        console.warn("API did not return array");
      }
    } catch (err) {
      console.error("Failed to fetch products:", err);
      setProducts([]);
    }
  }, [category, search, sort]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  // Handler to set category and scroll to products
  const handleCategorySelect = (cat) => {
    setCategory(cat);
    // Scroll to product section
    const el = document.getElementById("product-section");
    if (el) el.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="app-container">
      {/* Navbar */}
      <nav className="navbar">
        <h1>Smart Data Display</h1>
      </nav>

      <div className="main-content">
        {/* Hero section */}
        <Hero onCategorySelect={handleCategorySelect} />

        {/* Filter bar + products */}
        <div id="product-section">
          <FilterBar
            category={category}
            setCategory={setCategory}
            setSearch={setSearch}
            setSort={setSort}
          />

          {/* Safe map + fallback */}
          <div className="product-grid">
            {Array.isArray(products) && products.length > 0 ? (
              products.map((product, index) => (
                <ProductCard key={index} product={product} />
              ))
            ) : (
              <p className="no-products">No products found or failed to fetch data.</p>
            )}
          </div>
        </div>
      </div>

      {/* Floating Chatbot Icon and Panel */}
      <div>
        {/* Floating Icon */}
        {!showChatbot && (
          <button
            className="chatbot-float-icon"
            onClick={() => setShowChatbot(true)}
            aria-label="Open chatbot"
          >
            <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="18" cy="18" r="18" fill="#0d47a1"/>
              <path d="M10 24V12C10 10.8954 10.8954 10 12 10H24C25.1046 10 26 10.8954 26 12V20C26 21.1046 25.1046 22 24 22H14L10 26V24Z" fill="white"/>
            </svg>
          </button>
        )}
        {/* Floating Panel */}
        {showChatbot && (
          <div className="chatbot-float-panel">
            <button className="chatbot-close-btn" onClick={() => setShowChatbot(false)} aria-label="Close chatbot">×</button>
            <ChatbotBox />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
