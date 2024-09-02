import React, { useState } from 'react';
import './App.css';

function App() {
  const [keyword, setKeyword] = useState('');
  const [recommendations, setRecommendations] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await fetch(`http://csharp-container:4000/recommendations?keyword=${keyword}`);
      const data = await response.json();

      if (Array.isArray(data)) {
        setRecommendations(data);
      } else {
        setRecommendations([]);
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setRecommendations([]);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Book Recommendations</h1>
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="Enter keyword"
          className="search-input"
        />
        <button onClick={handleSearch} className="search-button">Search</button>
      </header>
      <main className="app-main">
        {recommendations.length > 0 ? (
          <ul className="recommendation-list">
            {recommendations.map((rec) => (
              <li key={rec.title} className="recommendation-item">
                <h2>{rec.title}</h2>
                <p>Rank: {rec.rank}</p>
                <p>Score: {rec.score.toFixed(3)}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No recommendations found.</p>
        )}
      </main>
    </div>
  );
}

export default App;



